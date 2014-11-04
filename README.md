Paper Drive
===========

A collection and filtering system for scientific papers and journal articles.

PDF files with a given name pattern are transformed to a searchable table of documents.<br/>

Sample directory structure:
```bash
.
├── pr
│   ├── Pattern recognition by means of disjoint principal components models - 1976 - 909c.pdf
│   ├── Pattern recognition by affine moment invariants - 1993 - 724c.pdf
│   └── Learning hierarchical features for scene labeling - 2013 - 91c.pdf
├── segmentation
│   ├── Object recognition from local scale-invariant features - 1999 - IEEE - 8369c.pdf
│   ├── Normalized Cuts and Image Segmentation - 2000 - 9351c.pdf
│   └── Comparing clusterings - an information based distance - 2007 - 510c.pdf
├── program.exe
└── readme.txt
```

The naming pattern of the PDF files has to be
```bash
<title>[ - <year>][ - <publisher>][ - <number_of_citations>c].pdf
```

A good estimate for the number of citations can be found at [google scholar](http://scholar.google.com/).
