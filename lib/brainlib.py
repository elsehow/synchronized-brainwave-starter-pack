import numpy as np
from scipy import stats
from scipy.interpolate import interp1d

#  https://github.com/wazaahhh/brainlib
#  by wazaahhh
#

def pSpectrum(vector):
    '''get the power spectrum of a vector of raw EEG data'''
    A = np.fft.fft(vector)
    ps = np.abs(A)**2
    ps = ps[:len(ps)/2]
    return ps

def entropy(power_spectrum,q=1):
    '''get the entropy of a power spectrum'''
    q = float(q)
    power_spectrum = np.array(power_spectrum)
    if not q == 1:
        S = 1/(q-1)*(1-np.sum(power_spectrum**q))
    else:
        S = - np.sum(power_spectrum*np.log2(power_spectrum))
    return S

def binnedPowerSpectra (pspectra,nbin):
    '''compress an array of power spectra into vectors of length nbins'''
    l = len(pspectra)
    array = np.zeros([l,nbin])

    for i,ps in enumerate(pspectra):
        x = np.arange(1,len(ps)+1)
        f = interp1d(x,ps)#/np.sum(ps))
        array[i] = f(np.arange(1, nbin+1))

    index = np.argwhere(array[:,0]==-1)
    array = np.delete(array,index,0)
    return array

def avgPowerSpectrum (arrayOfPowerSpectra, modifierFn):
    '''
    get the mean of an array of power spectra, and apply modifierFn to it
    example:
    avgPowerSpectrum(binnedPowerSpectra(pspectra,100), np.log10)
    '''
    return modifierFn(np.mean(arrayOfPowerSpectra, 0))

def avgPercentileUp (arrayOfPowerSpectra, confidenceIntervalParameter):
    '''confidenceIntervalParameter of 1 is 1%-99%'''
    return np.percentile(spectra,100-confidenceIntervalParameter,axis=0)

def avgPercentileDown (arrayOfPowerSpectra, confidenceIntervalParameter):
    return np.percentile(spectra,confidenceIntervalParameter,axis=0)

def pinkNoiseCharacterize(pspectrum,normalize=True,plot=False):
    '''Compute main power spectrum characteristics'''
    if normalize:
        pspectrum = pspectrum/np.sum(pspectrum)

    S = entropy(pspectrum,1)

    x = np.arange(1,len(pspectrum)+1)
    lx = np.log10(x)
    ly = np.log10(pspectrum)

    c1 = (x > 0)*(x < 80)
    c2 = x >= 80

    fit1 = stats.linregress(lx[c1],ly[c1])
    fit2 = stats.linregress(lx[c2],ly[c2])

    return {'S':S,'slope1':fit1[0],'slope2':fit2[0]}
