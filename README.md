Paper Drive
===========

A collection and filtering system for scientific papers and journal articles.

![Collection screenshot, sorted by number of citations](https://cloud.githubusercontent.com/assets/8630763/6443884/720ad0c0-c0fa-11e4-8816-17f1e29c5f7d.png)

PDF files with a given name pattern are transformed to a searchable table of documents.<br/>

Sample directory structure:
```bash
.
├── pr
│   ├── Pattern recognition by means of disjoint principal components models - 1976 - 909c.pdf
│   ├── Pattern recognition by affine moment invariants - 1993 - 724c.pdf
│   └── 01_Learning hierarchical features for scene labeling - 2013 - 91c.pdf
├── segmentation
│   ├── 00_Object recognition from local scale-invariant features - 1999 - IEEE - 8369c.pdf
│   ├── Normalized Cuts and Image Segmentation - 2000 - 9351c.pdf
│   └── Comparing clusterings - an information based distance - 2007 - 510c.pdf
├── program.exe
└── readme.txt
```

The naming pattern of the PDF files has to be
```bash
[<rating>_]<title>[ - <year>][ - (<author>)][ - <publisher>][ - <number_of_citations>c].pdf
```
Where `rating` ranges from top `00` to `config_data['max_rating']`. This inverse naming scheme enhances readability in file listings such as *ls*.

A good estimate for the number of citations can be found at [google scholar](http://scholar.google.com/).
