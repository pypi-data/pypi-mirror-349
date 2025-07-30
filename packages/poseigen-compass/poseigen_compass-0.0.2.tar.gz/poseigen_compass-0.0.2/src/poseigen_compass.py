import numpy as np
import pandas as pd
import os
import copy
import glob, shutil
#-----------------------------
import poseigen_seaside.basics as se
import poseigen_seaside.metrics as mex
#-----------------------------


def VarTra_exp(inp, inverse = False): 
    # TRICK IS YOU DO REVNUMBERS AFTER IN THE CALL 
    return np.log(inp) if inverse == False else np.exp(inp)

def RevNumbers(inp, min = 0, max = 10): 
    return max - inp + min 

def RandomCanGen(VarDict, num_can, num_gen = 10, configspace = False): 

    # NO LHC HERE. 

    # adding num_gen which multiplies num_can so that we get UNIQUE ones. 

    num_cangen = num_can * num_gen
    
    NewCanDict = {}
    
    if configspace is False: 

        GenCanDict = {}
        for i in range(num_cangen): GenCanDict[i] = {}

        sample = np.random.uniform(size = (num_cangen, len(VarDict))) #creates random numbers between 0 and 1

        for ik, key in enumerate(VarDict): 
            if VarDict[key][1] == 'cat':
                lvk = len(VarDict[key][0])
                c = np.random.choice(range(lvk), size = num_cangen)
                r = [VarDict[key][0][u] for u in c]
                    
            else: 
                n,m = VarDict[key][0][0], VarDict[key][0][1]
                
                if len(VarDict[key]) > 2: 
                    n,m = (VarDict[key][2](q) for q in (n,m))
                
                g = sample[:, ik] * (m - n) + n
                
                if len(VarDict[key]) > 2: 
                    g = [VarDict[key][2](jj, inverse = True) for jj in g]

                    if VarDict[key][2] == VarTra_exp: 
                        g = RevNumbers(g, VarDict[key][0][0], VarDict[key][0][1])

                r = np.round(g).astype(int) if VarDict[key][1] == 'int' else g
                r = r.tolist()

            for i in range(num_cangen): GenCanDict[i][key] = r[i]

        # NOW TO GET UNIQUE: 
    
        NewCanDict = se.UniqueNestedDict(GenCanDict, keepkey = False)
        NewCanDict = {k:v for k,v in NewCanDict.items() if k < num_can}
        
    
    else: 
        configs = VarDict.sample_configuration(int(num_can))
        for i in range(num_can): NewCanDict[i] = dict(configs[i])
        
    return NewCanDict



################################################################################

def StandardCanScorer(algo, algo_args, data, Splits = None, metrics_mode= [mex.AError, {}], add_metrics_modes = None, 
                     pathname = None, returnmodel = False): 

    #add_metrics_mode is optional but if specified is a list of functions and a list of their respective arguments. 

    if Splits is not None: dataz = [[d[Splits[s][t]] for d in data] for t in [0,1]]
    elif isinstance(data, dict): dataz = data[data.keys[s]]
    else: dataz = data

    m = algo(**algo_args)
    m.fit(*dataz[0])
    y_hat = m.predict(dataz[1][0])
    score = metrics_mode[0](y_hat, *dataz[1][1:], **metrics_mode[1])
    
    if pathname is not None: se.PickleDump(m, pathname)

    add_scores = []
    if add_metrics_modes is not None: 
        lamm = len(add_metrics_modes) // 2
        for amm in range(lamm): 
            add_scores.append(add_metrics_modes[amm](y_hat, *dataz[1][1:], **metrics_mode[amm+lamm]))
        
        score = [score, add_scores]
        
    return score if returnmodel is False else (score, m)




################################################################################


def ModelEvalHelper(c, 
                    algo, CanDict, data, Splits = None, repeats = 1, 
                    CS_mode = [StandardCanScorer, {'metrics_mode': [mex.AError, {'expo': 2}]}], CSDict = {}, 
                    lmd = 1, lsp = 1, 
                    statusprints = True, pathname = None, savemodels = False, pn_Can = None):

    #Sept 25 modification: Data splitting is handled by the scorer. 
        
    i, s, r = c

    Split = Splits[s] if Splits is not None else None

    if statusprints: 
        if r == 0 and s == 0:
            itos = CanDict[i].items() if statusprints == True else [(k, CanDict[i][k]) for k in statusprints]
            print(f' Model {i+1} of {lmd}: {itos}')
        print(f' cross val {s+1} of {lsp}, Repeat {r+1} of {repeats}')

    savepath = None
    if pathname is not None and savemodels == True:
        savepath = pathname + str(i) + '_' + str(s) + '_' + str(r)

    meh_args = {}
    if data is not None: meh_args['data'] = data
    if Split is not None: meh_args['Split'] = Split
    score = CS_mode[0](algo, CanDict[i], **meh_args,
                    pathname = savepath, **CSDict[i])

    if statusprints: print(f" Model {i+1}, cross val {s+1}, Repeat {r+1}: {score}")

    return score

def CanEvaluator(algo, CanDict, data, Splits = None, repeats = 1, parallel = False, 
                 CS_mode = [StandardCanScorer, {'metrics_mode': [mex.AError, {'expo': 2}]}], CS_vars = None, 
                 pickup = False, statusprints = True, pathname = None, savemodels = False,
                 ext = None): 
    
    #June 29, ADDED PARALLELIZATION! 
    
    #For YAHPO gym, adding a data is None option. If Data is None, it is assumed to be a surrogate operation. 


    if ext is True: ext = 'CanEval'
    newpathname = se.NewFolder(pathname, ext = ext)
    
    if pathname is None: pickup = False
    else: pn_met = newpathname + 'Mets' + '.p'
        
    CDK = CanDict.keys()  
    lmd = len(CDK)
    
    CSDict = {} 
    for i in CDK: 
        CSDict[i] = CS_mode[1]
        if CS_vars is not None: 
            x = {v: CanDict[i][v] for v in CS_vars}
            CSDict[i].update(x)
            for v in CS_vars: 
                del CanDict[i][v]
    
    #Each split has to be in the format: [array, array] 
    lsp = 1
    if Splits is not None: 
        if isinstance(Splits[0], list) is False: Splits = [Splits]
        lsp = len(Splits)
    elif isinstance(data, dict): lsp = len(data)

    modelcombos = []
    newmetrics = {} 
    for i in CDK:
        newmetrics[i] = {}
        for s in range(lsp):
            newmetrics[i][s] = {}
            for r in range(repeats):
                newmetrics[i][s][r] = None
                modelcombos.append([i, s, r])

    if pickup and os.path.isfile(pn_met): 
        oldmetrics = se.PickleLoad(pn_met)
        for i in oldmetrics.keys():
            if i < lmd: 
                for s in oldmetrics[i].keys():
                    for r in oldmetrics[i][s].keys(): 
                        newmetrics[i][s][r] = oldmetrics[i][s][r]
    
    print(newmetrics)
    
    MEH_args = {'algo': algo, 'CanDict': CanDict, 'data': data, 'Splits': Splits, 'repeats': repeats, 
                'CS_mode': CS_mode, 'CSDict': CSDict, 'lmd': lmd, 'lsp': lsp, 
                'statusprints': statusprints, 'pathname': newpathname, 'savemodels': savemodels} 

    #BELOW NEEDS WORK SINCE CHANGING METRICS TO A DICTIONARY 
    #if parallel > 1: #Needs to be an int > 1
        #pool = multiprocessing.Pool(parallel)
        #metrics = pool.map(*pack_function_for_map(ModelEvalHelper, modelcombos[len(metrics):], **MEH_args))
        #if pathname is not None: pickle.dump(metrics, open(pathname + pn_CEMe + '.p', 'wb'))
    #else #benefit of non-parallel is the pickup. Can we do pickup with 
    
    for c in modelcombos:
        i, s, r = c
        if newmetrics[i][s][r] is None: 
            newmetrics[i][s][r] = ModelEvalHelper(c, **MEH_args)
            if pathname is not None: se.PickleDump(newmetrics, pn_met)            
    
    return newmetrics





def RandomOpt(algo, VarDict, data, Splits = None, 
              budget = 20, repeats = 1, 
              CS_mode = [StandardCanScorer, {'metrics_mode': [mex.AError, {'expo': 2}]}], CS_vars = None,
              RMG_args = {}, configspace = False, 

              smallest = None, #PLACEHOLDER, DOESNT DO SHIT
              
              pickup = False, statusprints = True, pathname = None, savemodels = False, ext = None): 
        
    ######################################################
    
    if ext is True: ext = 'RandomOpt'
    newpathname = se.NewFolder(pathname, ext = ext)

    #--------------------------
    if pathname is not None: 

        CS_args = copy.deepcopy(CS_mode[1])
        if 'trainer_args' in CS_args.keys(): 
            for xo in ['inps', 'out', 'out_bind']: 
                CS_args['trainer_args'][xo] = None

        RO_args = {'VarDict': VarDict, 'CS_mode': [CS_mode[0], CS_args]}

        se.PickleDump(RO_args, newpathname + 'RO_args')
    #--------------------------

    if pathname is None: pickup = False
    else: pn_OO = newpathname + 'Out' + '.p'
    
    if pickup and os.path.isfile(pn_OO):

        CanDict, metrics = se.PickleLoad(pn_OO)
        
        # the following is an option to add more candidates in first round
        lcdk = len(CanDict[0].keys())
        difo = budget - lcdk

        if difo < 0: 
            for i in list(CanDict[0].keys()):
                if i >= budget: del CanDict[0][i]

        if difo > 0: # DOES NOT GUARANTEE UNIQUE ONES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            print('adding more')

            moreCanDict = RandomCanGen(VarDict, difo * 20, **RMG_args) #WE TRY DIFO * 20 FOR MROE CHANCE OF UNIQUE. 

            cdo = copy.deepcopy(CanDict)
            cdo[0].update({k+lcdk: v for k,v in moreCanDict.items()})
            CanDict = se.UniqueNestedDict(cdo, keepkey = False) #THEN RESETS NUMBER 
            CanDict = {0: {k:v for k,v in CanDict[0].items() if k < budget}} #BOOM. 

        for i in list(CanDict.keys()): 
            if i > 0: del CanDict[i]
        
        se.PickleDump([CanDict, metrics], pn_OO)
        
    else: 
        CanDict, metrics = {}, {}
        RMG_args.update({'configspace': configspace})
        CanDict[0] = RandomCanGen(VarDict, budget, **RMG_args)
        if newpathname is not None: se.PickleDump([CanDict, metrics], pn_OO)

    ######################################################

    #to filter out keys that are only 1 value in statusprints 

    sps = statusprints
    if statusprints:
        sps = []
        for key, val in VarDict.items(): 
            if val[1] == 'cat': 
                if len(val[0]) > 1: sps.append(key)
            else: sps.append(key)

    ######################################################

    ro = 0

    pn_can = newpathname + str(ro) if pathname is not None else None

    metrics[ro] = CanEvaluator(algo, CanDict[ro], data, 
                               Splits = Splits, repeats = repeats, 
                               CS_vars = CS_vars, CS_mode = CS_mode,
                               pickup = pickup, statusprints = sps, 
                               pathname = pn_can, savemodels = savemodels, ext = ext)

    OptOut = [CanDict, metrics]
    if newpathname is not None: se.PickleDump(OptOut,pn_OO)

        
    return OptOut



def Metrics2Flat(metrics): 
    #metrics is now a dictionary where it is Model, Split, Repeat
    flatmetrics = []
    for i in metrics.keys(): 
            for s in metrics[i].keys(): 
                for r in metrics[i][s].keys(): 
                    flatmetrics.append(metrics[i][s][r])
    return np.array(flatmetrics)



#############################################################################################

def TopCan(OptOut, num_top = 10, 
            reduce_func = None, smallest = True, 
            perround = False, ext = None):
            
            # fromidxs = None,
            # savemodels = False, ext = None): 
    
    #reduce_func summarizes the scores. 
    #perround returns the best cans per round. useful for optotp testing. 

    #This function just returns the best candidates(s) per round or general. 
    # If its per round, it returns a list of lists. If its not, it returns an array where each row has the [round, cand]
    
    # Also, currently applies the reduce func over all splits and repeats. 

    if isinstance(OptOut, str):

        if ext is True: ext = 'SurvOpt'
        newpathname = se.NewFolder(OptOut, ext = ext)
        CanDict, metrics = se.PickleLoad(newpathname + 'Out')

    else: CanDict, metrics = OptOut

    if reduce_func is None: reduce_func = np.nanmin if smallest else np.nanmax
    k = 1 if smallest else -1


    met_reduced = [np.array([reduce_func([metrics[k1][k2][k3][k4] 
                              for k3 in metrics[k1][k2].keys() 
                              for k4 in metrics[k1][k2][k3].keys()])
                              for k2 in metrics[k1].keys()]) for k1 in metrics.keys()]

    if perround is False: 

        met_reduced_comb = np.concatenate(met_reduced)
        round_idxs = np.concatenate([np.repeat(im, len(met)) for im, met in enumerate(met_reduced)])
        can_idxs = np.concatenate([np.arange(len(met)) for met in met_reduced])
        idxs_to_use = np.argsort(met_reduced_comb)[::k][:num_top]
        top_idxs = np.array([x[idxs_to_use] for x in [round_idxs, can_idxs]]).T

    else: 

        top_idxs = [np.array([np.repeat(imet, num_top), np.argsort(met)[::k][:num_top]]).T
                              for imet, met in enumerate(met_reduced)] 

    return top_idxs


def TopCanDict(OptOut, topcan, comb_rounds = True, ext = None):

    if isinstance(OptOut, str):

        if ext is True: ext = 'SurvOpt'
        newpathname = se.NewFolder(OptOut, ext = ext)
        CanDict, metrics = se.PickleLoad(newpathname + 'Out')

    else: CanDict, metrics = OptOut 

    if isinstance(topcan, list) is False: topcan = [topcan]

    if comb_rounds: NewCanDict = {str(tc[0]) + '_' + str(tc[1]): CanDict[tc[0]][tc[1]] 
                                  for tx in topcan for tc in tx}
    
    else: NewCanDict = {tx[0, 0]: {tc[1]: CanDict[tc[0]][tc[1]] for tc in tx} 
                        for tx in topcan}
    
    return NewCanDict


def TopCanGetData(pathname, newpathname, topcan,
                  indiv_folders = True, #Gathers into individual folders
                  noget = None):
    # automatically combines into new folder and gives you topcandict. 

    if isinstance(topcan, list) is False: topcan = [topcan]

    newpn = se.NewFolder(newpathname)

    for tx in topcan: 

        pn_tx = se.NewFolder(pathname + str(tx[0][0]))

        for tc in tx: 

            tc_prefix = str(tc[1]) + '_'
            targnames = glob.glob(pn_tx + tc_prefix + '*')

            if noget is not None: 
                if isinstance(noget, list) is False: noget = [noget]
                targnames = [tn for tn in targnames if not any(tg in tn for tg in noget)]

            new_tc_prefix = str(tc[0]) + '_' + str(tc[1])
 
            new_tc_prefix = se.NewFolder(newpn + new_tc_prefix) if indiv_folders else newpn + new_tc_prefix + '_'
        
            newnames = [new_tc_prefix + t[len(pn_tx) + len(tc_prefix):] for t in targnames]

            for t,n in zip(targnames, newnames): shutil.copyfile(t, n)
    
    return





#################################################

# ENSEMBLE STUFF #

def PredScorer(pred, 
               out, out_std = None, out_weights = None, out_bind = None,
               split = None, metrics_mode = None,
               pred_modif_mode = None):
    
    if pred_modif_mode is not None: pred = pred_modif_mode[0](pred, **pred_modif_mode[1])
    
    pred_sp, out_sp = [[xo[s] for s in split] for xo in [pred, out]]

    ozx = []
    for oz in [out_std, out_weights, out_bind]:
        if oz is not None: 
            ozx.append([oz[s] for s in split])
        else: ozx.append([None] * len(split))
    
    out_std_sp, out_weights_sp, out_bind_sp = ozx
    
    mets = []
    for ps, os, ss, ws, bs in zip(pred_sp, out_sp, out_std_sp, out_weights_sp, out_bind_sp): 

        mm_args = copy.deepcopy(metrics_mode[1])

        if ss is not None: mm_args['std'] = ss
        if ws is not None: mm_args['weights'] = ws
        if bs is not None: mm_args['bind'] = bs

        me = metrics_mode[0](ps, os, **mm_args)
        mets.append(me) 
    
    return np.array(mets) #Should be a 1 dim vector




def remove_outliers(inp, std_cutoff = 2, ddof = 0, return_idx = True):
    #inp is a 1 dim list of vals
    inp = np.array(inp) # just in case
    ret = np.where(abs(inp - np.mean(inp)) < std_cutoff * np.std(inp, ddof = ddof))[0]
    if return_idx is False: 
        ret = inp[ret]
    return ret if return_idx else inp[ret]

def EnsembleIdxs(pn, std_cutoff = 2, ddof = 1):
    #pn is that path to the folder
    mets = se.PickleLoad(pn + 'Mets')[0]
    mets2 = [y for x,y in mets.items()]
    return  remove_outliers(mets2, std_cutoff=std_cutoff, ddof = ddof, return_idx = True)

def EnsembleScorer(preds,
                   out, out_std = None, out_weights = None, out_bind = None,                  

                   split = None, metrics_mode = None,
                   score_on = 1,
                   std_cutoff = None, ddof = 1, 
                   top = None, smallest = True, 
                   pred_modif_mode = None, 
                   pathname = None, return_extra = False): 
    # split is [train, stoppage, xx, xx] 
    # The std_cutoff is based on the performance on the stoppage set. 
    # preds is a list of preds where the length is each observation

    #load_idx_keep is a pathname to go and get the idx_keep from. 

    if isinstance(preds[0], str): preds = [se.PickleLoad(p) for p in preds]
    preds = np.array(preds) 



    ##################################

    ps_args = {'out': out, 'out_std': out_std, 
               'out_weights': out_weights, 'out_bind': out_bind,
               'split': split, 'metrics_mode': metrics_mode, 
               'pred_modif_mode': pred_modif_mode}

    mets_all = np.array([PredScorer(pred, **ps_args) for pred in preds])

    stop_mets = mets_all[:, score_on] if len(mets_all.shape) > 1 else mets_all
    
    if std_cutoff is not None: 
        idx_keep = remove_outliers(stop_mets, std_cutoff=std_cutoff, 
                                ddof = ddof, return_idx = True)
    elif top is not None: 
        k = 1 if smallest else -1
        idx_keep = np.argsort(stop_mets)[::k][:top]
    
    else: idx_keep = np.arange(len(stop_mets))

    preds_keep = preds[idx_keep]
    
    ##################################

    preds_ensemb = np.mean(preds_keep, axis = 0)
    preds_ensemb_scores = PredScorer(preds_ensemb, **ps_args)

    if pathname is not None: 
        for g, gn in zip([idx_keep, preds_keep, preds_ensemb, preds_ensemb_scores], 
                         ['idx', 'preds_keep', 'preds', 'scores']):
            se.PickleDump(g, pathname + 'ensemble_' + gn)

    return (preds_ensemb_scores, preds_ensemb, idx_keep) if return_extra else preds_ensemb_scores


def Bootstrapper(inp, mode = [], iters = 100, 
                 boots_idx = None,
                 pathname = None,
                 
                 updates = 10, return_idx = False):
    
    inp = np.array(inp)
    li = len(inp)
    rango = np.arange(li)

    bs_idx = np.array([np.random.choice(rango, size = li, replace = True) 
                       for _ in np.arange(iters)]) if boots_idx is None else boots_idx
    
    prods = []
    for nidx, idx in enumerate(bs_idx): 
        prods.append(mode[0](inp[idx], **mode[1]))
        if updates is not None:
            if nidx % updates == 0: print(f'finished {nidx}')
    
    if pathname is None: 
        prods = np.array([mode[0](inp[idx], **mode[1]) for idx in bs_idx])
    else: 
        prods = np.array([mode[0](inp[idx], **mode[1],
                                  pathname = se.NewFolder(pathname + str(im))) 
                                  for im, idx in enumerate(bs_idx)])

    return (prods, bs_idx) if return_idx else prods

def PairwiseBootstrapper(inp1, inp2, 
                        mode1 = [], mode2 = [],
                        iters = 10, updates = None):
    
    #performs boostrapping on two inputs using mode1 and then does mode2 to compare the bootstrap inps. 

    prods1 = Bootstrapper(inp1, mode = mode1, iters = iters, updates = updates)
    prods2 = Bootstrapper(inp2, mode = mode1, iters = iters, updates = updates)

    return mode2[0](prods1, prods2, **mode2[1])

def BootstrapConfidenceInterval(inp, alpha = 0.95, 
                                onesided = None,
                                axis = None): 
    
    #can be onsided 'greater' or 'lesser'. 

    if onesided is None: 
        alx = (1-alpha) / 2
        p_lower = alx * 100
        p_higher = (1-alx) * 100
    elif onesided == 'lesser': 
        p_lower = 0
        p_higher = alpha * 100
    elif onesided == 'greater':
        p_lower = (1 - alpha) * 100
        p_higher = 100

    return np.array([np.percentile(np.sort(inp), p, axis = axis) for p in [p_lower, p_higher]])

def BootstrapStandardError(inp, ddof = 0, axis = None): 
    
    return np.std(inp, ddof = ddof, axis = axis)




