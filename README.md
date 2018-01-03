# Botnet-Finder-Framework
### A modular framework for botnet detectors prototyping and evaluation

In this work we present Botnet Finder Framework (BFF) a modular framework
for botnet detectors evaluation and a practical application of the framework for research purpose.
A botnet is a network of machines that are infected by a malware controlled 
by an attacker in order to perform illegitimate actions. Once a machine
becomes infected it joins the malware network and the owner of the
botnet (called botmaster) can perform several malicious or illegal actions
remotely controlling the bot.

In order to prevent botnet spreading or at least to block malicious traffic,
detection algorithm has been developed. Detectors should distinguish between
benign and malicious traffic accessing to network data. Most of state of the
art detectors use statistical approaches to extract relevant features
from data to identify malicious behaviors. Thereafter, they can detect
malicious communications between botmasters and infected machines analyzing
those features. Security research in this field is still on looking for developing
more precise algorithms.

This work provides a modular framework for botnet detectors prototyping and evaluation.
Moreover, we provide two reimplementation of botnet detectors (DISCLOSURE [1] and Bot-Track [2]).
We used this framework in order to evaluate the detectability of the botnet ELISA [3] (the
extension of this paper will be submitted at IEEE Transactions on Dependable and Secure Computing (TDSC)
2018 regular issue).

See my bachelor ![thesis](https://github.com/nicola-decao/Botnet-Finder-Framework/blob/master/NicolaDeCaoThesis.pdf) for further details.

### References
[1]  Leyla Bilge, Davide Balzarotti, William Robertson, Engin Kirda, and
Christopher Kruegel. DISCLOSURE: Detecting Botnet Command and
Control Servers Through Large-Scale NetFlow Analysis. 28th Annual
Computer Security Applications Conference, pages 129–138, 2012.

[2]  Jérôme François, Shaonan Wang, Radu State, and Thomas Engel. Bot-
Track: Tracking Botnets Using NetFlow and PageRank. IFIP Network-
ing 2011, pages 1–14, 2011.

[3]  Alberto Compagno, Mauro Conti, Daniele Lain, Giulio Lovisotto, and
Luigi Vincenzo Mancini. Boten ELISA: A novel approach for botnet
C&C in Online Social Networks. IEEE Conference on Communications
and Network Security (CNS), 2015, pages 74–82, 2015.

