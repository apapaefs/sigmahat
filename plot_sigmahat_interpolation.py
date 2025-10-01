import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import ticker, cm
from matplotlib.ticker import MultipleLocator

###################################
# read in data from a pickle file
###################################
def read_pickle(inputfile):
    inputstream = open(inputfile, 'br')
    data = pickle.load(inputstream)
    return data

##################################
# simple plot of interpolator
##################################
def plot(interp, m2i, m3i, plot_type):
    infile = plot_type + '.dat'
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # for LinearNDInterpolator
    #X = np.linspace(min(m2i), max(m2i))
    #Y = np.linspace(min(m3i), max(m3i))
    m2X, m3Y = np.meshgrid(m2i, m3i)

    # interpolate:
    zi = interp(m2X, m3Y)
    print(np.shape(zi))
    zi = zi.reshape((len(m2i),len(m3i)))
    
    # choose between types of plots:
    if plot_type == 'resonant_scan_unity':
        levels=np.arange(0,3.5E-9,0.5E-10)
        label=r'$\hat{\sigma}_u$ [pb/GeV$^2$], LHC@13.6 TeV'
    else:
        print('PLOT TYPE NOT DEFINED! PLEASE DEFINE IN FUNCTION')

    # contour plot of the interpolation:
    im = plt.contourf(m2i, m3i, zi, cmap='Spectral', levels=levels)
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(label, rotation=270, fontsize=20, labelpad=30)
    cbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    
    # block out the m3 < m2 + 125 region:
    ax.fill_between(m2i, m3i, where=m3i>=0, interpolate=True, color='white')
    ax.plot(m2i, m3i, lw=6, color='black')
    
    # set limits:
    ax.set_xlim(257,700)
    ax.set_ylim(np.min(m3i),900)

    # set labels
    ax.set_xlabel(r'$m_2$ [GeV]', fontsize=20)
    ax.set_ylabel(r'$m_3$ [GeV]', fontsize=20)

    # add text for excluded region:
    ax.text(500, 550, '$m_3 < m_2 + m_1$', fontsize=20)

    # set ticks
    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_minor_locator(MultipleLocator(25))
    ax.yaxis.set_major_locator(MultipleLocator(50))
    ax.yaxis.set_minor_locator(MultipleLocator(25))


    print('output in ' + infile.replace('.dat','.pdf'))
    plt.savefig(infile.replace('.dat','.pdf'), bbox_inches='tight')
    plt.close(fig)
    return zi


######################################################################
# plot the interpolation for all couplings = 1, m2m3xsec_interp      #
######################################################################

# arrays for region of validity of M2, M3
M2min = 260
M2max = 1060
M2array = np.linspace(M2min,M2max,160)
M2array_p = list(M2array)
M2array_p = [260-5.03144654] + M2array_p
M2array_p = np.array(M2array_p)
M3array_p = np.array(M2array_p + 125)

# read the pickle file
m2m3xsec_interp = read_pickle('sigmahat_interpolated_13.6.pkl')

# EXAMPLE of how to access a random element:
M2ex=500
M3ex=750
print('sighmahat at M2,M3=', M2ex, M3ex, '=', m2m3xsec_interp(M2ex, M3ex), 'pb/GeV^2)

# plot: 
xsec = plot(m2m3xsec_interp, M2array_p, M3array_p, 'resonant_scan_unity')
