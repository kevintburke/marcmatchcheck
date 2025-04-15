# marcmatchcheck
Compares different versions of the same MARC records across key fields (ISBN, author, title, edition, publisher, publication date, and physical description) by matching on 001. Requires input of two .mrc files with matching 001s and returns .csv with key fields and similarity score using fuzz.WRatio.

_NOTE: The original version of this program was created with the assistance of Microsoft Copilot and Meta AI. This version has been fully reviewed manually, but may still include some inefficiencies. Use with caution._

<b>Inputs</b><br>
&bull;Two .mrc (MARC Binary) files with matching 001 fields (e.g., different versions of the same records)<br>

<b>Outputs</b><br>
&bull;Uniquely named output file with key fields from records and average similarity score<br>
&bull;Non-unique files from process for use troubleshooting<br>

<b>Function</b><br>
&bull;Accepts text arguments for file names (without extensions)<br>
&bull;Retrieves key fields from records using <a href="https://pymarc.readthedocs.io/en/latest/#" title="PyMarc Documentation">PyMarc</a> including: ISBN (020, first occurrence only), author (100, 110, or 111), title (245 $a and $b), edition statement (250) publisher (260 $b or 264 $b), publication date (260 $c or 264 $c), physical description (300)<br>
&bull;Creates two dataframes, one for each input file<br>
&bull;Merges the dataframes using 001 as the key<br>
&bull;Calculates similarity between record A and recrd B<br>
&nbsp;&nbsp;&nbsp;&nbsp;&bull;Returns 100 for exact ISBN match (including None) or 0 for mis-match<br>
&nbsp;&nbsp;&nbsp;&nbsp;&bull;Uses fuzz.WRatio to calculate similarity of all other fields (including None)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&bull;Returns average of all similarity scores rounded to two decimal places<br>
&bull;Adds column with similarity scores to start of dataframe with merged records and sorts on similarity score
&bull;Writes results to a new CSV using timestamp (month, day, hour, minute) to avoid overwriting earlier outputs
