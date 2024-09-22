def simulation_identifier(params, extension=None):
    L = float(params['L'])
    T = int(params['T'])
    DX = float(params['DX'])
    DY = float(params['DY'])
    D = float(params['D'])
    K1 = float(params['K1'])
    K2 = float(params['K2'])
    K3 = float(params['K3'])

    if extension is None:
        return f'[L,T,DX,DY,D,K]=[{L},{T},{DX},{DY},{D},{(K1,K2,K3)}]'

    return f'[L,T,DX,DY,D,K]=[{L},{T},{DX},{DY},{D},{(K1,K2,K3)}].{extension}'