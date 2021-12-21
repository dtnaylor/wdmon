#!/usr/bin/env python3

import numpy as np
import sys

from collections import namedtuple
import xml.etree.ElementTree as ET

Sample = namedtuple("Sample", "id timestamp snr rssi rate noise")

def get_samples(root):
    for child in root:
        if "type" in child.attrib and child.attrib["type"] == "WDSIGNALGRAPHSAMPLE":
            yield child

def parse_sample(sample):
    return Sample(
        sample.attrib["id"],
        sample.find("./attribute[@name='timestamp']").text,
        int(sample.find("./attribute[@name='snr']").text),
        int(sample.find("./attribute[@name='rssi']").text),
        float(sample.find("./attribute[@name='rate']").text),
        int(sample.find("./attribute[@name='noise']").text),
    )

def print_summary(samples):
    snrs = [s.snr for s in samples]
    print("SNR:")
    print(f"  min/p25/med/p75/max:\t{np.min(snrs)}/{np.percentile(snrs, 25)}/{np.median(snrs)}/{np.percentile(snrs, 75)}/{np.max(snrs)}")
    print(f"                 mean:\t{np.mean(snrs):.2f}")
    
    rates = [s.rate for s in samples]
    print("Tx Rate:")
    print(f"  min/p25/med/p75/max:\t{np.min(rates)}/{np.percentile(rates, 25)}/{np.median(rates)}/{np.percentile(rates, 75)}/{np.max(rates)}")
    print(f"                 mean:\t{np.mean(rates):.2f}")

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    samples = [parse_sample(s) for s in get_samples(root)]

    print_summary(samples)

if __name__ == "__main__":
    main()
