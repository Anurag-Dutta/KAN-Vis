# `KAN-Vis`: Efficient and Lightweight Visual Technique for Network Traffic Classification using Kolmogorov-Arnold Network

_Anurag Dutta_, _Pallavi Anand_, _Sangita Roy_, and _Rajat Subhra Chakraborty_

Network traffic classification is increasingly challenging due to encryption, VPNs, and anonymization like Tor. We propose a visual classifier, `KAN-Vis` using packet-size histogram time-series with the Kolmogorov-Arnold Network (KAN). Our four `KAN-Vis` deep learning models optimize accuracy and computational cost, achieving state-of-the-art results on the `ISCXTor-nonTor` dataset: 93.61% accuracy for Tor traffic (**previous best: 67.8%**) and 96.54% for non-Tor traffic (**previous best: ~85%**). Unlike previous approaches, we also perform intra-class classification, supporting both encrypted and unencrypted traffic while maintaining privacy.
