#!/usr/bin/env python3

import argparse
import numpy as np
import os
import sys

from collections import namedtuple
import xml.etree.ElementTree as ET

Sample = namedtuple("Sample", "id timestamp snr rssi rate noise")

def get_samples(file):
    tree = ET.parse(file)
    root = tree.getroot()
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

def print_ascii_summary(name, samples):
    def summarize_feature(values):
        print(f"  min/p25/med/p75/max:\t{np.min(values)}/{np.percentile(values, 25)}/{np.median(values)}/{np.percentile(values, 75)}/{np.max(values)}")
        print(f"                 mean:\t{np.mean(values):.2f}")
    
    print("="*10 + f" {name} " + "="*10)

    snrs = [s.snr for s in samples]
    print("SNR:")
    summarize_feature(snrs)
    
    rates = [s.rate for s in samples]
    print("Tx Rate:")
    summarize_feature(rates)


def print_csv_summary(name, samples):
    def summarize_feature(values):
        return f"{np.mean(values)},{np.min(values)},{np.percentile(values, 25)},{np.median(values)},{np.percentile(values, 75)},{np.max(values)}"
    
    snrs = [s.snr for s in samples]
    rates = [s.rate for s in samples]
    print(f"{name},{summarize_feature(snrs)},{summarize_feature(rates)}")


def main(args):
    if args.csv:
        print("file,mean-snr,min-snr,p25-snr,median-snr,p75-snr,max-snr,mean-rate,min-rate,p25-rate,median-rate,p75-rate,max-rate")

    for file in args.files:
        samples = [parse_sample(s) for s in get_samples(file)]
        if args.csv:
            print_csv_summary(os.path.basename(file), samples)
        else:
            print_ascii_summary(os.path.basename(file), samples)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", help=".wdmon WiFi performance trace files")
    parser.add_argument("--csv", action="store_true", help="Print results as CSV")

    main(parser.parse_args())
