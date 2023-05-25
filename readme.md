# CV HTML-YAML Generator

## Export to PDF

To export the generated output.html to a pdf you have to open it in a browser.
Then you have to open the print settings for the file.
Here you have to change the following values:
 - Border: None
 - Print Background
 - Remove Print Header and Footer 


## Hot Reloading while changing template
Just start the watcher script with 
```
python watcher.py
```

If you open the output.html in a browser you just have to hit refresh to get the newest changes.

Alternatively, you can also open the output.html with a html server, e.g. with vs code you can right click on the file and select *Open with Live Server*. If you chose this method you don't have to refresh and always see the newest update.
However, you still have to start the watcher script beforehand.

## Compress the pdf file for printers

Use the following command to compress the created pdf file.
```
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output-compressed.pdf output.html.pdf
```

Change output.html.pdf to your created pdf file.