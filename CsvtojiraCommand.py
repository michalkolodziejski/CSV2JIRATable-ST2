'''
Provides action for formatting CSV as WIKI/JIRA Table.

@author: Michal Kolodziejski <michal.kolodziejski@gmail.com>
@license: GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt)
@since: 2013-12-31
'''
import sublime, sublime_plugin, re, subprocess, datetime

DEFAULT_IS_ENABLED = True
DEBUG_IS_ENABLED = True

st_version = 2
if sublime.version() == '' or int(sublime.version()) > 3000:
        st_version = 3

class CsvtojiraCommand(sublime_plugin.TextCommand):
	def setClipboardData(self, data):
	    sublime.set_clipboard(data)

	def normalize_line_endings(self, string):
		line_endings = self.view.settings().get('default_line_ending')

		string = string.replace('\r\n', '\n').replace('\r', '\n')
		if line_endings == 'windows':
			string = string.replace('\n', '\r\n')
		elif line_endings == 'mac':
			string = string.replace('\n', '\r')
		return string

	def delete_blank_lines(self, string):
		line_endings = self.view.settings().get('default_line_ending')

		if line_endings == 'windows':
			string = string.replace('\r\n\r\n', '\r\n')
		elif line_endings == 'mac':
			string = string.replace('\r\r', '\r')
		else: # unix
			string = string.replace('\n\n', '\n')
		return string

	def logPrint(self, level, string):
		print "###" + " " + str(datetime.datetime.now()) + " " + "("+level+")" + " " + string

	def debugPrint(self, string):
		if DEBUG_IS_ENABLED:
			self.logPrint("debug", string)

	def infoPrint(self, string):
		self.logPrint("info", string)

	def run(self, edit):

		self.debugPrint("START")

		self.infoPrint("loading settings...")

		settings = sublime.load_settings('CsvtojiraCommand.sublime-settings')  

		columnSeparator = settings.get('column_separator')
		headerSeparator = settings.get('header_separator')
		defaultLineEnding = settings.get('default_line_ending')
		nationalCharacters = settings.get('national_characters')
		normalizeLineEndings = settings.get('normalize_line_endings')
		deleteBlankLines = settings.get('delete_blank_lines')
		inputSeparator = settings.get('input_separator')
		processOnlySelection = settings.get('process_only_selection')

		self.debugPrint("* column_separator: "+columnSeparator)
		self.debugPrint("* header_separator: "+headerSeparator)
		self.debugPrint("* national_characters: "+nationalCharacters)
		self.debugPrint("* default_line_ending: "+':'.join('0x'+x.encode('hex') for x in str(defaultLineEnding)))
		self.debugPrint("* normalize_line_endings: "+str(normalizeLineEndings))
		self.debugPrint("* delete_blank_lines: "+str(deleteBlankLines))
		self.debugPrint("* input_separator: "+':'.join('0x'+x.encode('hex') for x in str(inputSeparator)))
		self.debugPrint("* process_only_selection: "+str(processOnlySelection))
		
		returnValue = ""
		inputText = ""

		if processOnlySelection:
			inputRegions = self.view.sel()
		else:
			inputRegions = [sublime.Region(0, self.view.size())]

		for region in inputRegions:
			input = self.view.substr(region)
			# view = self.view.sel()

			self.infoPrint("input characters="+str(region.end()-region.begin()))
			
			# if region.empty():
				# return

			rowNumber = 1
	        
			# lines = view.lines(sublime.Region(0, view.size()))

			lines = self.view.lines(region)

			self.infoPrint("input lines="+str(len(lines)))

			# special thanks to Max Shawabkeh for this REGEXP (http://stackoverflow.com/questions/2212933/python-regex-for-reading-csv-like-rows)

			r = re.compile(r"""
			    \s*                # Any whitespace.
			    (                  # Start capturing here.
			      [^""" + re.escape(inputSeparator) + r""""']*?         # Either a series of non-comma non-quote characters.
			      |                # OR
			      "(?:             # A double-quote followed by a string of characters...
			          [^"\\]|\\.   # That are either non-quotes or escaped...
			       )*              # ...repeated any number of times.
			      "                # Followed by a closing double-quote.
			      |                # OR
			      '(?:[^'\\]|\\.)*'# Same as above, for single quotes.
			    )                  # Done capturing.
			    \s*                # Allow arbitrary space before the comma.
			    (?:""" + re.escape(inputSeparator) + r"""|$)            # Followed by a comma or the end of a string.
			    """, re.VERBOSE)

			returnValue = ""

			for line in lines:
				string = self.view.substr(line)
		
				if (normalizeLineEndings):
					string = self.delete_blank_lines(string).strip()
				
				if (deleteBlankLines):
					string = self.normalize_line_endings(string)

				string = string.encode('ascii',nationalCharacters)

				if len(string) == 0:
					rowNumber += 1
					continue

				if rowNumber == 1:
					currentSeparator = headerSeparator
				else:
					currentSeparator = columnSeparator

				returnValue += currentSeparator+(currentSeparator.join(r.findall(string)))+defaultLineEnding

				rowNumber += 1

			self.debugPrint("output: " + returnValue)

			self.infoPrint("copying output to clipboard!")

			self.setClipboardData(returnValue)

			self.debugPrint("STOP")