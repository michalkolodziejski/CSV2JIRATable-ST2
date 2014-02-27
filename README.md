# CSV2JIRATable-ST2

**Tool for converting CSV file to JIRA/Wiki table format in SublimeText 2.**
This is a [Sublime Text 2](http://www.sublimetext.com/2) plugin.

## Description
CSV2JIRATable is a plugin for Sublime Text 2 that allows you to convert CSV formatted data to JIRA formatted table.

## Installation

Go to your `Packages` subdirectory under ST2's data directory:

* Windows: `%APPDATA%\Sublime Text 2`
* OS X: `~/Library/Application Support/Sublime Text 2/Packages`
* Linux: `~/.config/sublime-text-2`
* Portable Installation: `Sublime Text 2/Data`

Then clone this repository:

    git clone git://github.com/mkolodziejski/CSV2JIRATable-ST2.git

That's it!

## Usage
***Current version assumes, that there is a header in first row of processed data, and formats it differently (using "header_separator" from settings as a separator character). If Your data don't have a header, just replace it by yourself, or change "header_separator" to the same value as "column_separator".***

Many applications (JIRA, Confluence, etc.) have input format for tables as defined in [markup specification](https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=tables). But applications that process data, are assuming (correctly!) that the standard format is CSV [Comma Separated Values](http://en.wikipedia.org/wiki/Comma-separated_values), and JIRA and other applications does not accept such data format.

### CSV Format
```
A,B,C
1,2,3
4,5,6
```

### Expected output

| A | B | C |
| --- | --- | --- |
| 1 | 2 | 3 |
| 4 | 5 | 6 |

To achive this, the CSV format data have to be converted to JIRA format.

### JIRA format
```
||A||B||C||
|1|2|3|
|4|5|6|
```

After opening the CSV file in Sublime Text 2, it is now possible to convert to `JIRA format`. There are two possibilities:

1. using a shortcut `ctrl+alt+j`
2. using a context menu: ***(rightclick) on opened file*** `CSV2JIRA -> Convert & Copy`

***This plugin copies converted text to clipboard***

## Options
Some options are available to customize the plugin behaviour. The
config keys goes into config files accessible throught the "Preferences"
menu.

``` js
{
	"normalize_line_endings" : true,
	"delete_blank_lines" : true,	
	"national_characters" :  "xmlcharrefreplace",
	"default_line_ending" : "\n",
	"column_separator" : "|",
	"header_separator" : "||"
}
```

### Column separator (default: "|")
This setting determines what character (or string) is to be used to separate columns in output.

``` js
{
"column_separator" :  "|"
}
```

### Header separator (default: "||")
This setting determines what character (or string) is to be used to separate HEADER columns in output.

``` js
{
"header_separator" :  "||"
}
```

### National characters (default: "xmlcharrefreplace")
This setting determines what to do with a "national characters" which are outside ASCII range.

``` js
{
"national_characters" :  "xmlcharrefreplace"
}
```

Value | Description
------- | ---------
'ignore' | removes the national characters
'replace' | replaces with ?
'xmlcharrefreplace' | turn into xml entities
'strict' | will throw UnicodeEncodeErrors if found any non-unicode character

### Normalize line engings (default: "true")
This setting determines if line endings should be normalized.

``` js
{
"normalize_line_endings" : true
}
```

**Algorithm**
1. Take the text
2. replace "\r\n" with "\n"
3. replace "\r" with "\n" <- now we have all the endings as "\n".
4. replace "\n" with desired line ending (based on system settings)

Type (standard) | Normalized value
------- | ---------
windows | '\r\n' 
mac     | '\r'

### Delete blank lines (default: "true")
This setting determines if "blank" (empty) lines shoul be ignored or processed. As blank line is considered to have consecutive line endings).

``` js
{
"delete_blank_lines" : true
}
```

Type (standard) | Input value | Output value
------- | --------- | ---------
windows | '\r\n\r\n' | '\r\n' 
mac     | '\r\r'     | '\r'
unix    | '\n\n'		| '\n'

### Default line ending (default: "\n")
This setting determines what character should be used to end a line in output.

``` js
{
"default_line_ending" : "\n"
}
```

### Input separator (default: "\t")
This setting determines added input_separator parameter to chose which character to treat as separator while parsing input lines.
``` js
{
"input_separator" : "\t"
}
```

### Process only selection (default: "true")
This setting determines if plugin should process a whole file (when set to "false") or only the selected text in view (when set to "true")
``` js
{
"process_only_selection" : true
}
```

## Credits
***Special thanks to Max Shawabkeh for his REGEXP (http://stackoverflow.com/questions/2212933/python-regex-for-reading-csv-like-rows)***

It all started by 'scratching own itch' - plugin created solely for my own consumption. Then I've decided to share it with ST2 users-community.

## History

2013-12-31

* Initial version.

2014-02-12

* Fixed issue #1 https://github.com/michalkolodziejski/CSV2JIRATable-ST2/issues/1

2014-02-14

* added parameter "input_separator" to set separator character/string for columns in input text

2014-02-27

* added parameter "process_only_selection" to determine if plugin should process a whole file (when set to "false") or only the selected text in view (when set to "true") (Fixed issue #2 https://github.com/michalkolodziejski/CSV2JIRATable-ST2/issues/2)

## Problems?

[Submit an issue](https://github.com/michalkolodziejski/CSV2JIRATable-ST2/issues).