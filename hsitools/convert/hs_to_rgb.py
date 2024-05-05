import os
import numpy as np

def hs2rgb(hsi: np.array, lower_limit_wavelength: int=350, upper_limit_wavelength: int=1100, spectrum_stepsize: int=5, color_matching_function: np.array = None):
    '''
    Parameters:
        hsi (np.array): hyperspectral image (height, width, band)
        lower_limit_wavelength (int): lower limit wavelength of hsi
        upper_limit_wavelength (int): upper_limit_wavelength of hsi
        spectrum_stemsize (int): wavelength range between hsi channels
        color_matching_function (np.array): color matching function

    Returns:
        np.array: NumPy array of RGB images converted from hyperspectral images
    '''

    hsi = hsi.astype(np.float32)
    height, width = hsi.shape[0], hsi.shape[1]

    if color_matching_function == None:
        color_matching_function = get_10_deg_XYZ_CMFs()
        color_matching_function = color_matching_function[::spectrum_stepsize] 

    wave_length = np.arange(lower_limit_wavelength, upper_limit_wavelength + 1, spectrum_stepsize)

    index_low, index_hight = int(np.where(wave_length == color_matching_function[0, 0])[0]), int(np.where(wave_length == color_matching_function[-1, 0])[0]) + 1

    hsi_cie_range = hsi[:, :, index_low : index_hight]

    img_xyz = np.zeros((height, width, 3))
    img_rgb = np.zeros((height, width, 3))

    M = np.array([[0.41844, -0.15866, -0.08283],
                  [-0.09117, 0.25242, 0.01570],
                  [0.00092, -0.00255, 0.17858]])
    
    intensity = hsi_cie_range.reshape(-1, index_hight - index_low)
    
    xyz = np.dot(intensity, color_matching_function[:, 1:])

    img_xyz = xyz.reshape(height, width, 3)

    img_rgb = np.dot(img_xyz, M.T)

    img_rgb = ((img_rgb - np.min(img_rgb)) / (np.max(img_rgb) - np.min(img_rgb)) * 255).astype(np.uint8)

    img_rgb_gamma  = gamma_correction(img_rgb, gamma=1.9, max_value=255)
    return img_rgb_gamma

def gamma_correction(img: np.array, gamma: float=2.2, max_value: int=65535, base_max_value: int=255):
    
    img = img.astype(np.float32) / max_value
    img = img ** (1.0 / gamma)
    img = img * base_max_value
    if base_max_value == 255:
        img = img.astype(np.uint8)
    elif base_max_value == 65535:
        img = img.astype(np.uint16)

    return img

def get_10_deg_XYZ_CMFs():
    array = np.array((390,2.952420E-03,4.076779E-04,1.318752E-02,
                      391,3.577275E-03,4.977769E-04,1.597879E-02,
                      392,4.332146E-03,6.064754E-04,1.935758E-02,
                      393,5.241609E-03,7.370040E-04,2.343758E-02,
                      394,6.333902E-03,8.929388E-04,2.835021E-02,
                      395,7.641137E-03,1.078166E-03,3.424588E-02,
                      396,9.199401E-03,1.296816E-03,4.129467E-02,
                      397,1.104869E-02,1.553159E-03,4.968641E-02,
                      398,1.323262E-02,1.851463E-03,5.962964E-02,
                      399,1.579791E-02,2.195795E-03,7.134926E-02,
                      400,1.879338E-02,2.589775E-03,8.508254E-02,
                      401,2.226949E-02,3.036799E-03,1.010753E-01,
                      402,2.627978E-02,3.541926E-03,1.195838E-01,
                      403,3.087862E-02,4.111422E-03,1.408647E-01,
                      404,3.611890E-02,4.752618E-03,1.651644E-01,
                      405,4.204986E-02,5.474207E-03,1.927065E-01,
                      406,4.871256E-02,6.285034E-03,2.236782E-01,
                      407,5.612868E-02,7.188068E-03,2.582109E-01,
                      408,6.429866E-02,8.181786E-03,2.963632E-01,
                      409,7.319818E-02,9.260417E-03,3.381018E-01,
                      410,8.277331E-02,1.041303E-02,3.832822E-01,
                      411,9.295327E-02,1.162642E-02,4.316884E-01,
                      412,1.037137E-01,1.289884E-02,4.832440E-01,
                      413,1.150520E-01,1.423442E-02,5.379345E-01,
                      414,1.269771E-01,1.564080E-02,5.957740E-01,
                      415,1.395127E-01,1.712968E-02,6.568187E-01,
                      416,1.526661E-01,1.871265E-02,7.210459E-01,
                      417,1.663054E-01,2.038394E-02,7.878635E-01,
                      418,1.802197E-01,2.212935E-02,8.563391E-01,
                      419,1.941448E-01,2.392985E-02,9.253017E-01,
                      420,2.077647E-01,2.576133E-02,9.933444E-01,
                      421,2.207911E-01,2.760156E-02,1.059178E+00,
                      422,2.332355E-01,2.945513E-02,1.122832E+00,
                      423,2.452462E-01,3.133884E-02,1.184947E+00,
                      424,2.570397E-01,3.327575E-02,1.246476E+00,
                      425,2.688989E-01,3.529554E-02,1.308674E+00,
                      426,2.810677E-01,3.742705E-02,1.372628E+00,
                      427,2.933967E-01,3.967137E-02,1.437661E+00,
                      428,3.055933E-01,4.201998E-02,1.502449E+00,
                      429,3.173165E-01,4.446166E-02,1.565456E+00,
                      430,3.281798E-01,4.698226E-02,1.624940E+00,
                      431,3.378678E-01,4.956742E-02,1.679488E+00,
                      432,3.465097E-01,5.221219E-02,1.729668E+00,
                      433,3.543953E-01,5.491387E-02,1.776755E+00,
                      434,3.618655E-01,5.766919E-02,1.822228E+00,
                      435,3.693084E-01,6.047429E-02,1.867751E+00,
                      436,3.770107E-01,6.332195E-02,1.914504E+00,
                      437,3.846850E-01,6.619271E-02,1.961055E+00,
                      438,3.918591E-01,6.906185E-02,2.005136E+00,
                      439,3.980192E-01,7.190190E-02,2.044296E+00,
                      440,4.026189E-01,7.468288E-02,2.075946E+00,
                      441,4.052637E-01,7.738452E-02,2.098231E+00,
                      442,4.062482E-01,8.003601E-02,2.112591E+00,
                      443,4.060660E-01,8.268524E-02,2.121427E+00,
                      444,4.052283E-01,8.538745E-02,2.127239E+00,
                      445,4.042529E-01,8.820537E-02,2.132574E+00,
                      446,4.034808E-01,9.118925E-02,2.139093E+00,
                      447,4.025362E-01,9.431041E-02,2.144815E+00,
                      448,4.008675E-01,9.751346E-02,2.146832E+00,
                      449,3.979327E-01,1.007349E-01,2.142250E+00,
                      450,3.932139E-01,1.039030E-01,2.128264E+00,
                      451,3.864108E-01,1.069639E-01,2.103205E+00,
                      452,3.779513E-01,1.099676E-01,2.069388E+00,
                      453,3.684176E-01,1.129992E-01,2.030030E+00,
                      454,3.583473E-01,1.161541E-01,1.988178E+00,
                      455,3.482214E-01,1.195389E-01,1.946651E+00,
                      456,3.383830E-01,1.232503E-01,1.907521E+00,
                      457,3.288309E-01,1.273047E-01,1.870689E+00,
                      458,3.194977E-01,1.316964E-01,1.835578E+00,
                      459,3.103345E-01,1.364178E-01,1.801657E+00,
                      460,3.013112E-01,1.414586E-01,1.768440E+00,
                      461,2.923754E-01,1.468003E-01,1.735338E+00,
                      462,2.833273E-01,1.524002E-01,1.701254E+00,
                      463,2.739463E-01,1.582021E-01,1.665053E+00,
                      464,2.640352E-01,1.641400E-01,1.625712E+00,
                      465,2.534221E-01,1.701373E-01,1.582342E+00,
                      466,2.420135E-01,1.761233E-01,1.534439E+00,
                      467,2.299346E-01,1.820896E-01,1.482544E+00,
                      468,2.173617E-01,1.880463E-01,1.427438E+00,
                      469,2.044672E-01,1.940065E-01,1.369876E+00,
                      470,1.914176E-01,1.999859E-01,1.310576E+00,
                      471,1.783672E-01,2.060054E-01,1.250226E+00,
                      472,1.654407E-01,2.120981E-01,1.189511E+00,
                      473,1.527391E-01,2.183041E-01,1.129050E+00,
                      474,1.403439E-01,2.246686E-01,1.069379E+00,
                      475,1.283167E-01,2.312426E-01,1.010952E+00,
                      476,1.167124E-01,2.380741E-01,9.541809E-01,
                      477,1.056121E-01,2.451798E-01,8.995253E-01,
                      478,9.508569E-02,2.525682E-01,8.473720E-01,
                      479,8.518206E-02,2.602479E-01,7.980093E-01,
                      480,7.593120E-02,2.682271E-01,7.516389E-01,
                      481,6.733159E-02,2.765005E-01,7.082645E-01,
                      482,5.932018E-02,2.850035E-01,6.673867E-01,
                      483,5.184106E-02,2.936475E-01,6.284798E-01,
                      484,4.486119E-02,3.023319E-01,5.911174E-01,
                      485,3.836770E-02,3.109438E-01,5.549619E-01,
                      486,3.237296E-02,3.194105E-01,5.198843E-01,
                      487,2.692095E-02,3.278683E-01,4.862772E-01,
                      488,2.204070E-02,3.365263E-01,4.545497E-01,
                      489,1.773951E-02,3.456176E-01,4.249955E-01,
                      490,1.400745E-02,3.554018E-01,3.978114E-01,
                      491,1.082291E-02,3.660893E-01,3.730218E-01,
                      492,8.168996E-03,3.775857E-01,3.502618E-01,
                      493,6.044623E-03,3.896960E-01,3.291407E-01,
                      494,4.462638E-03,4.021947E-01,3.093356E-01,
                      495,3.446810E-03,4.148227E-01,2.905816E-01,
                      496,3.009513E-03,4.273539E-01,2.726773E-01,
                      497,3.090744E-03,4.398206E-01,2.555143E-01,
                      498,3.611221E-03,4.523360E-01,2.390188E-01,
                      499,4.491435E-03,4.650298E-01,2.231335E-01,
                      500,5.652072E-03,4.780482E-01,2.078158E-01,
                      501,7.035322E-03,4.915173E-01,1.930407E-01,
                      502,8.669631E-03,5.054224E-01,1.788089E-01,
                      503,1.060755E-02,5.197057E-01,1.651287E-01,
                      504,1.290468E-02,5.343012E-01,1.520103E-01,
                      505,1.561956E-02,5.491344E-01,1.394643E-01,
                      506,1.881640E-02,5.641302E-01,1.275353E-01,
                      507,2.256923E-02,5.792416E-01,1.163771E-01,
                      508,2.694456E-02,5.944264E-01,1.061161E-01,
                      509,3.199910E-02,6.096388E-01,9.682266E-02,
                      510,3.778185E-02,6.248296E-01,8.852389E-02,
                      511,4.430635E-02,6.399656E-01,8.118263E-02,
                      512,5.146516E-02,6.550943E-01,7.463132E-02,
                      513,5.912224E-02,6.702903E-01,6.870644E-02,
                      514,6.714220E-02,6.856375E-01,6.327834E-02,
                      515,7.538941E-02,7.012292E-01,5.824484E-02,
                      516,8.376697E-02,7.171103E-01,5.353812E-02,
                      517,9.233581E-02,7.330917E-01,4.914863E-02,
                      518,1.011940E-01,7.489041E-01,4.507511E-02,
                      519,1.104362E-01,7.642530E-01,4.131175E-02,
                      520,1.201511E-01,7.788199E-01,3.784916E-02,
                      521,1.303960E-01,7.923410E-01,3.467234E-02,
                      522,1.411310E-01,8.048510E-01,3.175471E-02,
                      523,1.522944E-01,8.164747E-01,2.907029E-02,
                      524,1.638288E-01,8.273520E-01,2.659651E-02,
                      525,1.756832E-01,8.376358E-01,2.431375E-02,
                      526,1.878114E-01,8.474653E-01,2.220677E-02,
                      527,2.001621E-01,8.568868E-01,2.026852E-02,
                      528,2.126822E-01,8.659242E-01,1.849246E-02,
                      529,2.253199E-01,8.746041E-01,1.687084E-02,
                      530,2.380254E-01,8.829552E-01,1.539505E-02,
                      531,2.507787E-01,8.910274E-01,1.405450E-02,
                      532,2.636778E-01,8.989495E-01,1.283354E-02,
                      533,2.768607E-01,9.068753E-01,1.171754E-02,
                      534,2.904792E-01,9.149652E-01,1.069415E-02,
                      535,3.046991E-01,9.233858E-01,9.753000E-03,
                      536,3.196485E-01,9.322325E-01,8.886096E-03,
                      537,3.352447E-01,9.412862E-01,8.089323E-03,
                      538,3.513290E-01,9.502378E-01,7.359131E-03,
                      539,3.677148E-01,9.587647E-01,6.691736E-03,
                      540,3.841856E-01,9.665325E-01,6.083223E-03,
                      541,4.005312E-01,9.732504E-01,5.529423E-03,
                      542,4.166669E-01,9.788415E-01,5.025504E-03,
                      543,4.325420E-01,9.832867E-01,4.566879E-03,
                      544,4.481063E-01,9.865720E-01,4.149405E-03,
                      545,4.633109E-01,9.886887E-01,3.769336E-03,
                      546,4.781440E-01,9.897056E-01,3.423302E-03,
                      547,4.927483E-01,9.899849E-01,3.108313E-03,
                      548,5.073315E-01,9.899624E-01,2.821650E-03,
                      549,5.221315E-01,9.900731E-01,2.560830E-03,
                      550,5.374170E-01,9.907500E-01,2.323578E-03,
                      551,5.534217E-01,9.922826E-01,2.107847E-03,
                      552,5.701242E-01,9.943837E-01,1.911867E-03,
                      553,5.874093E-01,9.966221E-01,1.734006E-03,
                      554,6.051269E-01,9.985649E-01,1.572736E-03,
                      555,6.230892E-01,9.997775E-01,1.426627E-03,
                      556,6.410999E-01,9.999440E-01,1.294325E-03,
                      557,6.590659E-01,9.992200E-01,1.174475E-03,
                      558,6.769436E-01,9.978793E-01,1.065842E-03,
                      559,6.947143E-01,9.961934E-01,9.673215E-04,
                      560,7.123849E-01,9.944304E-01,8.779264E-04,
                      561,7.299978E-01,9.927831E-01,7.967847E-04,
                      562,7.476478E-01,9.911578E-01,7.231502E-04,
                      563,7.654250E-01,9.893925E-01,6.563501E-04,
                      564,7.834009E-01,9.873288E-01,5.957678E-04,
                      565,8.016277E-01,9.848127E-01,5.408385E-04,
                      566,8.201041E-01,9.817253E-01,4.910441E-04,
                      567,8.386843E-01,9.780714E-01,4.459046E-04,
                      568,8.571936E-01,9.738860E-01,4.049826E-04,
                      569,8.754652E-01,9.692028E-01,3.678818E-04,
                      570,8.933408E-01,9.640545E-01,3.342429E-04,
                      571,9.106772E-01,9.584409E-01,3.037407E-04,
                      572,9.273554E-01,9.522379E-01,2.760809E-04,
                      573,9.432502E-01,9.452968E-01,2.509970E-04,
                      574,9.582244E-01,9.374773E-01,2.282474E-04,
                      575,9.721304E-01,9.286495E-01,2.076129E-04,
                      576,9.849237E-01,9.187953E-01,1.888948E-04,
                      577,9.970067E-01,9.083014E-01,1.719127E-04,
                      578,1.008907E+00,8.976352E-01,1.565030E-04,
                      579,1.021163E+00,8.872401E-01,1.425177E-04,
                      580,1.034327E+00,8.775360E-01,1.298230E-04,
                      581,1.048753E+00,8.687920E-01,1.182974E-04,
                      582,1.063937E+00,8.607474E-01,1.078310E-04,
                      583,1.079166E+00,8.530233E-01,9.832455E-05,
                      584,1.093723E+00,8.452535E-01,8.968787E-05,
                      585,1.106886E+00,8.370838E-01,8.183954E-05,
                      586,1.118106E+00,8.282409E-01,7.470582E-05,
                      587,1.127493E+00,8.187320E-01,6.821991E-05,
                      588,1.135317E+00,8.086352E-01,6.232132E-05,
                      589,1.141838E+00,7.980296E-01,5.695534E-05,
                      590,1.147304E+00,7.869950E-01,5.207245E-05,
                      591,1.151897E+00,7.756040E-01,4.762781E-05,
                      592,1.155582E+00,7.638996E-01,4.358082E-05,
                      593,1.158284E+00,7.519157E-01,3.989468E-05,
                      594,1.159934E+00,7.396832E-01,3.653612E-05,
                      595,1.160477E+00,7.272309E-01,3.347499E-05,
                      596,1.159890E+00,7.145878E-01,3.068400E-05,
                      597,1.158259E+00,7.017926E-01,2.813839E-05,
                      598,1.155692E+00,6.888866E-01,2.581574E-05,
                      599,1.152293E+00,6.759103E-01,2.369574E-05,
                      600,1.148163E+00,6.629035E-01,2.175998E-05,
                      601,1.143345E+00,6.498911E-01,1.999179E-05,
                      602,1.137685E+00,6.368410E-01,1.837603E-05,
                      603,1.130993E+00,6.237092E-01,1.689896E-05,
                      604,1.123097E+00,6.104541E-01,1.554815E-05,
                      605,1.113846E+00,5.970375E-01,1.431231E-05,
                      606,1.103152E+00,5.834395E-01,1.318119E-05,
                      607,1.091121E+00,5.697044E-01,1.214548E-05,
                      608,1.077902E+00,5.558892E-01,1.119673E-05,
                      609,1.063644E+00,5.420475E-01,1.032727E-05,
                      610,1.048485E+00,5.282296E-01,9.530130E-06,
                      611,1.032546E+00,5.144746E-01,8.798979E-06,
                      612,1.015870E+00,5.007881E-01,8.128065E-06,
                      613,9.984859E-01,4.871687E-01,7.512160E-06,
                      614,9.804227E-01,4.736160E-01,6.946506E-06,
                      615,9.617111E-01,4.601308E-01,6.426776E-06,
                      616,9.424119E-01,4.467260E-01,0.000000E+00,
                      617,9.227049E-01,4.334589E-01,0.000000E+00,
                      618,9.027804E-01,4.203919E-01,0.000000E+00,
                      619,8.828123E-01,4.075810E-01,0.000000E+00,
                      620,8.629581E-01,3.950755E-01,0.000000E+00,
                      621,8.432731E-01,3.828894E-01,0.000000E+00,
                      622,8.234742E-01,3.709190E-01,0.000000E+00,
                      623,8.032342E-01,3.590447E-01,0.000000E+00,
                      624,7.822715E-01,3.471615E-01,0.000000E+00,
                      625,7.603498E-01,3.351794E-01,0.000000E+00,
                      626,7.373739E-01,3.230562E-01,0.000000E+00,
                      627,7.136470E-01,3.108859E-01,0.000000E+00,
                      628,6.895336E-01,2.987840E-01,0.000000E+00,
                      629,6.653567E-01,2.868527E-01,0.000000E+00,
                      630,6.413984E-01,2.751807E-01,0.000000E+00,
                      631,6.178723E-01,2.638343E-01,0.000000E+00,
                      632,5.948484E-01,2.528330E-01,0.000000E+00,
                      633,5.723600E-01,2.421835E-01,0.000000E+00,
                      634,5.504353E-01,2.318904E-01,0.000000E+00,
                      635,5.290979E-01,2.219564E-01,0.000000E+00,
                      636,5.083728E-01,2.123826E-01,0.000000E+00,
                      637,4.883006E-01,2.031698E-01,0.000000E+00,
                      638,4.689171E-01,1.943179E-01,0.000000E+00,
                      639,4.502486E-01,1.858250E-01,0.000000E+00,
                      640,4.323126E-01,1.776882E-01,0.000000E+00,
                      641,4.150790E-01,1.698926E-01,0.000000E+00,
                      642,3.983657E-01,1.623822E-01,0.000000E+00,
                      643,3.819846E-01,1.550986E-01,0.000000E+00,
                      644,3.657821E-01,1.479918E-01,0.000000E+00,
                      645,3.496358E-01,1.410203E-01,0.000000E+00,
                      646,3.334937E-01,1.341614E-01,0.000000E+00,
                      647,3.174776E-01,1.274401E-01,0.000000E+00,
                      648,3.017298E-01,1.208887E-01,0.000000E+00,
                      649,2.863684E-01,1.145345E-01,0.000000E+00,
                      650,2.714900E-01,1.083996E-01,0.000000E+00,
                      651,2.571632E-01,1.025007E-01,0.000000E+00,
                      652,2.434102E-01,9.684588E-02,0.000000E+00,
                      653,2.302389E-01,9.143944E-02,0.000000E+00,
                      654,2.176527E-01,8.628318E-02,0.000000E+00,
                      655,2.056507E-01,8.137687E-02,0.000000E+00,
                      656,1.942251E-01,7.671708E-02,0.000000E+00,
                      657,1.833530E-01,7.229404E-02,0.000000E+00,
                      658,1.730097E-01,6.809696E-02,0.000000E+00,
                      659,1.631716E-01,6.411549E-02,0.000000E+00,
                      660,1.538163E-01,6.033976E-02,0.000000E+00,
                      661,1.449230E-01,5.676054E-02,0.000000E+00,
                      662,1.364729E-01,5.336992E-02,0.000000E+00,
                      663,1.284483E-01,5.016027E-02,0.000000E+00,
                      664,1.208320E-01,4.712405E-02,0.000000E+00,
                      665,1.136072E-01,4.425383E-02,0.000000E+00,
                      666,1.067579E-01,4.154205E-02,0.000000E+00,
                      667,1.002685E-01,3.898042E-02,0.000000E+00,
                      668,9.412394E-02,3.656091E-02,0.000000E+00,
                      669,8.830929E-02,3.427597E-02,0.000000E+00,
                      670,8.281010E-02,3.211852E-02,0.000000E+00,
                      671,7.761208E-02,3.008192E-02,0.000000E+00,
                      672,7.270064E-02,2.816001E-02,0.000000E+00,
                      673,6.806167E-02,2.634698E-02,0.000000E+00,
                      674,6.368176E-02,2.463731E-02,0.000000E+00,
                      675,5.954815E-02,2.302574E-02,0.000000E+00,
                      676,5.564917E-02,2.150743E-02,0.000000E+00,
                      677,5.197543E-02,2.007838E-02,0.000000E+00,
                      678,4.851788E-02,1.873474E-02,0.000000E+00,
                      679,4.526737E-02,1.747269E-02,0.000000E+00,
                      680,4.221473E-02,1.628841E-02,0.000000E+00,
                      681,3.934954E-02,1.517767E-02,0.000000E+00,
                      682,3.665730E-02,1.413473E-02,0.000000E+00,
                      683,3.412407E-02,1.315408E-02,0.000000E+00,
                      684,3.173768E-02,1.223092E-02,0.000000E+00,
                      685,2.948752E-02,1.136106E-02,0.000000E+00,
                      686,2.736717E-02,1.054190E-02,0.000000E+00,
                      687,2.538113E-02,9.775050E-03,0.000000E+00,
                      688,2.353356E-02,9.061962E-03,0.000000E+00,
                      689,2.182558E-02,8.402962E-03,0.000000E+00,
                      690,2.025590E-02,7.797457E-03,0.000000E+00,
                      691,1.881892E-02,7.243230E-03,0.000000E+00,
                      692,1.749930E-02,6.734381E-03,0.000000E+00,
                      693,1.628167E-02,6.265001E-03,0.000000E+00,
                      694,1.515301E-02,5.830085E-03,0.000000E+00,
                      695,1.410230E-02,5.425391E-03,0.000000E+00,
                      696,1.312106E-02,5.047634E-03,0.000000E+00,
                      697,1.220509E-02,4.695140E-03,0.000000E+00,
                      698,1.135114E-02,4.366592E-03,0.000000E+00,
                      699,1.055593E-02,4.060685E-03,0.000000E+00,
                      700,9.816228E-03,3.776140E-03,0.000000E+00,
                      701,9.128517E-03,3.511578E-03,0.000000E+00,
                      702,8.488116E-03,3.265211E-03,0.000000E+00,
                      703,7.890589E-03,3.035344E-03,0.000000E+00,
                      704,7.332061E-03,2.820496E-03,0.000000E+00,
                      705,6.809147E-03,2.619372E-03,0.000000E+00,
                      706,6.319204E-03,2.430960E-03,0.000000E+00,
                      707,5.861036E-03,2.254796E-03,0.000000E+00,
                      708,5.433624E-03,2.090489E-03,0.000000E+00,
                      709,5.035802E-03,1.937586E-03,0.000000E+00,
                      710,4.666298E-03,1.795595E-03,0.000000E+00,
                      711,4.323750E-03,1.663989E-03,0.000000E+00,
                      712,4.006709E-03,1.542195E-03,0.000000E+00,
                      713,3.713708E-03,1.429639E-03,0.000000E+00,
                      714,3.443294E-03,1.325752E-03,0.000000E+00,
                      715,3.194041E-03,1.229980E-03,0.000000E+00,
                      716,2.964424E-03,1.141734E-03,0.000000E+00,
                      717,2.752492E-03,1.060269E-03,0.000000E+00,
                      718,2.556406E-03,9.848854E-04,0.000000E+00,
                      719,2.374564E-03,9.149703E-04,0.000000E+00,
                      720,2.205568E-03,8.499903E-04,0.000000E+00,
                      721,2.048294E-03,7.895158E-04,0.000000E+00,
                      722,1.902113E-03,7.333038E-04,0.000000E+00,
                      723,1.766485E-03,6.811458E-04,0.000000E+00,
                      724,1.640857E-03,6.328287E-04,0.000000E+00,
                      725,1.524672E-03,5.881375E-04,0.000000E+00,
                      726,1.417322E-03,5.468389E-04,0.000000E+00,
                      727,1.318031E-03,5.086349E-04,0.000000E+00,
                      728,1.226059E-03,4.732403E-04,0.000000E+00,
                      729,1.140743E-03,4.404016E-04,0.000000E+00,
                      730,1.061495E-03,4.098928E-04,0.000000E+00,
                      731,9.877949E-04,3.815137E-04,0.000000E+00,
                      732,9.191847E-04,3.550902E-04,0.000000E+00,
                      733,8.552568E-04,3.304668E-04,0.000000E+00,
                      734,7.956433E-04,3.075030E-04,0.000000E+00,
                      735,7.400120E-04,2.860718E-04,0.000000E+00,
                      736,6.880980E-04,2.660718E-04,0.000000E+00,
                      737,6.397864E-04,2.474586E-04,0.000000E+00,
                      738,5.949726E-04,2.301919E-04,0.000000E+00,
                      739,5.535291E-04,2.142225E-04,0.000000E+00,
                      740,5.153113E-04,1.994949E-04,0.000000E+00,
                      741,4.801234E-04,1.859336E-04,0.000000E+00,
                      742,4.476245E-04,1.734067E-04,0.000000E+00,
                      743,4.174846E-04,1.617865E-04,0.000000E+00,
                      744,3.894221E-04,1.509641E-04,0.000000E+00,
                      745,3.631969E-04,1.408466E-04,0.000000E+00,
                      746,3.386279E-04,1.313642E-04,0.000000E+00,
                      747,3.156452E-04,1.224905E-04,0.000000E+00,
                      748,2.941966E-04,1.142060E-04,0.000000E+00,
                      749,2.742235E-04,1.064886E-04,0.000000E+00,
                      750,2.556624E-04,9.931439E-05,0.000000E+00,
                      751,2.384390E-04,9.265512E-05,0.000000E+00,
                      752,2.224525E-04,8.647225E-05,0.000000E+00,
                      753,2.076036E-04,8.072780E-05,0.000000E+00,
                      754,1.938018E-04,7.538716E-05,0.000000E+00,
                      755,1.809649E-04,7.041878E-05,0.000000E+00,
                      756,1.690167E-04,6.579338E-05,0.000000E+00,
                      757,1.578839E-04,6.148250E-05,0.000000E+00,
                      758,1.474993E-04,5.746008E-05,0.000000E+00,
                      759,1.378026E-04,5.370272E-05,0.000000E+00,
                      760,1.287394E-04,5.018934E-05,0.000000E+00,
                      761,1.202644E-04,4.690245E-05,0.000000E+00,
                      762,1.123502E-04,4.383167E-05,0.000000E+00,
                      763,1.049725E-04,4.096780E-05,0.000000E+00,
                      764,9.810596E-05,3.830123E-05,0.000000E+00,
                      765,9.172477E-05,3.582218E-05,0.000000E+00,
                      766,8.579861E-05,3.351903E-05,0.000000E+00,
                      767,8.028174E-05,3.137419E-05,0.000000E+00,
                      768,7.513013E-05,2.937068E-05,0.000000E+00,
                      769,7.030565E-05,2.749380E-05,0.000000E+00,
                      770,6.577532E-05,2.573083E-05,0.000000E+00,
                      771,6.151508E-05,2.407249E-05,0.000000E+00,
                      772,5.752025E-05,2.251704E-05,0.000000E+00,
                      773,5.378813E-05,2.106350E-05,0.000000E+00,
                      774,5.031350E-05,1.970991E-05,0.000000E+00,
                      775,4.708916E-05,1.845353E-05,0.000000E+00,
                      776,4.410322E-05,1.728979E-05,0.000000E+00,
                      777,4.133150E-05,1.620928E-05,0.000000E+00,
                      778,3.874992E-05,1.520262E-05,0.000000E+00,
                      779,3.633762E-05,1.426169E-05,0.000000E+00,
                      780,3.407653E-05,1.337946E-05,0.000000E+00,
                      781,3.195242E-05,1.255038E-05,0.000000E+00,
                      782,2.995808E-05,1.177169E-05,0.000000E+00,
                      783,2.808781E-05,1.104118E-05,0.000000E+00,
                      784,2.633581E-05,1.035662E-05,0.000000E+00,
                      785,2.469630E-05,9.715798E-06,0.000000E+00,
                      786,2.316311E-05,9.116316E-06,0.000000E+00,
                      787,2.172855E-05,8.555201E-06,0.000000E+00,
                      788,2.038519E-05,8.029561E-06,0.000000E+00,
                      789,1.912625E-05,7.536768E-06,0.000000E+00,
                      790,1.794555E-05,7.074424E-06,0.000000E+00,
                      791,1.683776E-05,6.640464E-06,0.000000E+00,
                      792,1.579907E-05,6.233437E-06,0.000000E+00,
                      793,1.482604E-05,5.852035E-06,0.000000E+00,
                      794,1.391527E-05,5.494963E-06,0.000000E+00,
                      795,1.306345E-05,5.160948E-06,0.000000E+00,
                      796,1.226720E-05,4.848687E-06,0.000000E+00,
                      797,1.152279E-05,4.556705E-06,0.000000E+00,
                      798,1.082663E-05,4.283580E-06,0.000000E+00,
                      799,1.017540E-05,4.027993E-06,0.000000E+00,
                      800,9.565993E-06,3.788729E-06,0.000000E+00,
                      801,8.995405E-06,3.564599E-06,0.000000E+00,
                      802,8.460253E-06,3.354285E-06,0.000000E+00,
                      803,7.957382E-06,3.156557E-06,0.000000E+00,
                      804,7.483997E-06,2.970326E-06,0.000000E+00,
                      805,7.037621E-06,2.794625E-06,0.000000E+00,
                      806,6.616311E-06,2.628701E-06,0.000000E+00,
                      807,6.219265E-06,2.472248E-06,0.000000E+00,
                      808,5.845844E-06,2.325030E-06,0.000000E+00,
                      809,5.495311E-06,2.186768E-06,0.000000E+00,
                      810,5.166853E-06,2.057152E-06,0.000000E+00,
                      811,4.859511E-06,1.935813E-06,0.000000E+00,
                      812,4.571973E-06,1.822239E-06,0.000000E+00,
                      813,4.302920E-06,1.715914E-06,0.000000E+00,
                      814,4.051121E-06,1.616355E-06,0.000000E+00,
                      815,3.815429E-06,1.523114E-06,0.000000E+00,
                      816,3.594719E-06,1.435750E-06,0.000000E+00,
                      817,3.387736E-06,1.353771E-06,0.000000E+00,
                      818,3.193301E-06,1.276714E-06,0.000000E+00,
                      819,3.010363E-06,1.204166E-06,0.000000E+00,
                      820,2.837980E-06,1.135758E-06,0.000000E+00,
                      821,2.675365E-06,1.071181E-06,0.000000E+00,
                      822,2.522020E-06,1.010243E-06,0.000000E+00,
                      823,2.377511E-06,9.527779E-07,0.000000E+00,
                      824,2.241417E-06,8.986224E-07,0.000000E+00,
                      825,2.113325E-06,8.476168E-07,0.000000E+00,
                      826,1.992830E-06,7.996052E-07,0.000000E+00,
                      827,1.879542E-06,7.544361E-07,0.000000E+00,
                      828,1.773083E-06,7.119624E-07,0.000000E+00,
                      829,1.673086E-06,6.720421E-07,0.000000E+00,
                      830,1.579199E-06,6.345380E-07,0.000000E+00))
    return array.reshape((441, 4))
