def simulation_identifier(params, extension=None):
    L = float(params['L'])
    T = int(params['T'])
    DX = float(params['DX'])
    DY = float(params['DY'])
    D = float(params['D'])
    K1 = float(params['K1'])
    K2 = float(params['K2'])
    K3 = float(params['K3'])
    MIXING_ENABLED = params['MIXING_ENABLED'] == 'True'
    T_MIX = int(params['T_MIX'])

    if extension is None:
        return f'[L,T,DX,DY,D,K,mix]=[{L},{T},{DX},{DY},{D},{(K1,K2,K3)},{T_MIX if MIXING_ENABLED else None}]'

    return f'[L,T,DX,DY,D,K,T_MIX]=[{L},{T},{DX},{DY},{D},{(K1,K2,K3)},{T_MIX if MIXING_ENABLED else None}].{extension}'