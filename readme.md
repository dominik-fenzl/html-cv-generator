# CV HTML-YAML Generator

## Export to PDF

To export the generated output.html to a pdf you have to open it in a browser.
Then you have to open the print settings for the file.
Here you have to change the following values:
 - Border: None
 - Print Background
 - Remove Print Header and Footer 


## Compress the pdf file for printers

Use the following command to compress the created pdf file.
```
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output-compressed.pdf output.html.pdf
```

Change output.html.pdf to your created pdf file.