import numpy as np


def cosine_dft():
    # Define the frequencies of the cosine curves
    frequencies = [1, 2, 3, 3.5, 4.2]  # Change the frequencies as desired

    # Generate the x-axis values
    x = np.linspace(0, 2 * np.pi, 1000)

    # Generate the cosine curves
    cosine_curves = np.array([np.cos(freq * x) for freq in frequencies])
    signal = cosine_curves.sum(axis=0)
    component_frequencies = np.arange(0, 6, 0.1)
    similarities = [np.dot(np.cos(i * x), signal) for i in component_frequencies]

    norm_simillarities = similarities / np.sum(similarities) * len(frequencies)
    # each freq max amplitude is 1, so if you have 5 freq, then max amp is now 5.
    # when u normalise, max amp is 1, so you multiply by 5 to match the signal

    reconstructed_signal = []

    for i, freq in enumerate(component_frequencies):
        weighted_signal = norm_simillarities[i] * np.cos(freq * x)
        reconstructed_signal.append(weighted_signal)

    reconstructed_signal = np.array(reconstructed_signal).sum(axis=0)

    plt.plot(reconstructed_signal)
    plt.plot(signal)


def sine_dft():
    # Define the frequencies of the sine curves
    frequencies = [1, 2, 3, 3.5, 4.2]  # Change the frequencies as desired

    # Generate the x-axis values
    x = np.linspace(0, 2 * np.pi, 1000)

    # Generate the sine curves
    sine_curves = np.array([np.sin(freq * x) for freq in frequencies])
    signal = sine_curves.sum(axis=0)
    component_frequencies = np.arange(0, 6, 0.1)
    similarities = [np.dot(np.sin(i * x), signal) for i in component_frequencies]

    norm_simillarities = similarities / np.sum(similarities) * len(frequencies)
    # each freq max amplitude is 1, so if you have 5 freq, then max amp is now 5.
    # when u normalise, max amp is 1, so you multiply by 5 to match the signal

    reconstructed_signal = []

    for i, freq in enumerate(component_frequencies):
        weighted_signal = norm_simillarities[i] * np.sin(freq * x)
        reconstructed_signal.append(weighted_signal)

    reconstructed_signal = np.array(reconstructed_signal).sum(axis=0)

    plt.plot(reconstructed_signal)
    plt.plot(signal)
