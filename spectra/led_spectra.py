import matplotlib.pyplot as plt
import numpy as np


def gaussian(wavelength , mu, sigma):
    """
    Generates a Gaussian distribution.

    Parameters:
    - wavelength: Array of wavelength values.
    - mu: Central wavelength (mean).
    - sigma: Standard deviation (controls the width).

    Returns:
    - Gaussian distribution normalized to have area = 1.
    """
    return (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((wavelength - mu)/sigma)**2)

def compute_weights(wavelengths):
    """
    Computes weights for each wavelength based on the spacing.
    
    Parameters:
    - wavelengths: Array of wavelengths (nm).
    
    Returns:
    - Weights corresponding to each wavelength.
    """
    weights = np.zeros_like(wavelengths, dtype=float)
    
    # Handle intermediate wavelengths
    for i in range(1, len(wavelengths) - 1):
        weights[i] = (wavelengths[i] - wavelengths[i - 1]) / 2 + (wavelengths[i + 1] - wavelengths[i]) / 2
    
    # Handle boundaries
    weights[0] = (wavelengths[1] - wavelengths[0])  # First weight
    weights[-1] = (wavelengths[-1] - wavelengths[-2])  # Last weight
    
    return weights

def load_hemoglobin_spectra(filepath):
    """
    Load hemoglobin spectra from a file.

    Parameters:
        filepath (str): Path to the file containing the spectra.

    Returns:
        wavelengths (np.ndarray): Array of wavelengths in nm.
        hb02 (np.ndarray): Array of HbO2 absorbance values.
        hb (np.ndarray): Array of Hb absorbance values.
    """
    wavelengths, hb02, hb = [], [], []
    
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith("#") or not line.strip():  # Skip comments and empty lines
                continue
            parts = line.split()
            wavelengths.append(float(parts[0]))
            hb02.append(float(parts[1]))
            hb.append(float(parts[2]))
    
    return np.array(wavelengths), np.array(hb02), np.array(hb)

#hgl spectrum helper
def plotHglSpectra(wavelengths, hb02, hb):
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, hb02, label="HbO2", color='red')
    plt.plot(wavelengths, hb, label="Hb", color='blue')
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Absorbance (cm⁻¹/M)")
    plt.title("Hemoglobin Absorption Spectra")
    plt.legend()
    plt.grid(True)
    plt.show()

#hgl spectrum helper along with computed averages
def plotHglSpectraCompare(wavelengths, hbO2, hb, avg_hbO2, avg_hb):
    graph_window_start = 500
    graph_window_end = 1000
    plt.figure(figsize=(10, 6))
    plt.yscale('log')
    plt.xlim(graph_window_start, graph_window_end)
    plt.ylim(200, 60000)
    plt.plot(wavelengths, hbO2, label="HbO2 real", color='red')
    plt.plot(wavelengths, hb, label="Hb real", color='blue')
    #assume the 9 values in the array are located at 550, 600, 650, 700, 750, 800, 850, 900, 950
    xaxis = [550, 600, 650, 700, 750, 800, 850, 900, 950]
    plt.scatter(xaxis, avg_hbO2, color='red', label="HbO2 LED")
    plt.scatter(xaxis, avg_hb, color='blue', label="Hb LED")
    plt.xlabel("Lungime de unda (nm)")
    plt.ylabel("Absorbanța specifică (cm⁻¹/M)")
    plt.title("Spectre de absorbtie a hemoglobinei")
    plt.legend()
    plt.grid(True)
    plt.show()

#led spectrum helper
def plotLEDSpectra(wavelengths, led_spectra):
    graph_window_start = 500
    graph_window_end = 1000
    plt.figure(figsize=(14, 6))
    plt.xlim(graph_window_start, graph_window_end)
    for i in range(len(led_spectra)):
        plt.plot(wavelengths, led_spectra[i], label=f"LED {i + 1}")
    plt.xlabel("Lungime de undă (nm)")
    plt.ylabel("Intensitate relativă")
    plt.title("Spectre LED")
    plt.legend()
    plt.grid(True)
    plt.show()
    
#plot all the stuff togetha
def plotAll(wavelengths, hbO2, hb, led_spectra, avg_hbO2, avg_hb):
    #labelurile aici le bagam po romanski ca sa punem pe licenta
    graph_window_start = 500
    graph_window_end = 1000
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    plt.yscale('log')
    plt.xlim(graph_window_start, graph_window_end)
    plt.ylim(200, 60000)
    plt.plot(wavelengths, hbO2, label="HbO2 real", color='red')
    plt.plot(wavelengths, hb, label="Hb real", color='blue')
    xaxis = [550, 600, 650, 700, 750, 800, 850, 900, 950]
    plt.scatter(xaxis, avg_hbO2, color='red', label="HbO2 LED")
    plt.scatter(xaxis, avg_hb, color='blue', label="Hb LED")
    plt.xlabel("Lungime de unda (nm)")
    plt.ylabel("Absorbanța specifică (cm⁻¹/M)")
    plt.title("Spectre de absorbtie a hemoglobinei")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.xlim(graph_window_start, graph_window_end)
    for i in range(len(led_spectra)):
        plt.plot(wavelengths, led_spectra[i], label=f"LED {i + 1}")
    plt.xlabel("Lungime de undă (nm)")
    plt.ylabel("Intensitate relativă")
    plt.title("Spectre LED")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()


def main():
    file_path = "spectra/hemoglobinSpectra.txt"
    wavelengths, hbO2, hb = load_hemoglobin_spectra(file_path)

    # Plot the hemoglobin spectra
    #plotHglSpectra(wavelengths, hbO2, hb)

    # Get LED spectra 550 to 950
    #remember ur 650 is actually 660 cos of LED supplier company
    led_wavelengths = [550, 600, 660, 700, 750, 800, 850, 900, 950]
    led_sigmas = [20, 20, 20, 20, 20, 20, 20, 20, 20]

    led_spectra = []
    for i in range(len(led_wavelengths)):
        led_spectra.append(gaussian(wavelengths, led_wavelengths[i], led_sigmas[i]))

    # Plot the LED spectra
    #plotLEDSpectra(wavelengths, led_spectra)

    # Get weights for each wavelength
    weights = compute_weights(wavelengths)

    # Compute the absorbance for each LED
    absorbances_hbO2 = []
    absorbances_hb = []
    for spectrum in led_spectra:
        absorbance_hbO2 = np.sum(spectrum * hbO2 * weights) / np.sum(spectrum * weights)
        absorbance_hb = np.sum(spectrum * hb * weights) / np.sum(spectrum * weights)
        absorbances_hbO2.append(absorbance_hbO2)
        absorbances_hb.append(absorbance_hb)
  
    #print results
    np.set_printoptions(precision=6, suppress=True)

    print("Absorbances HbO2:",  np.array(absorbances_hbO2))
    print("Absorbances Hb:",  np.array(absorbances_hb))

    # Plot the comparison
    # plotLEDSpectra(wavelengths, led_spectra)
    # Plot the hemoglobin spectra with averages
    plotHglSpectraCompare(wavelengths, hbO2, hb, absorbances_hbO2, absorbances_hb)
    
    # Plot all together
    #plotAll(wavelengths, hbO2, hb, led_spectra, absorbances_hbO2, absorbances_hb)

if __name__ == '__main__':
    main()