# -*- coding: utf-8 -*-
import pyparsing as pyp
import sys
import contextlib
import csv

STR_VALUE = pyp.QuotedString("'", escChar='\\', multiline=True)
NUMBER_VALUE = pyp.Optional(pyp.Literal('-')) + pyp.Word(pyp.nums + '.')
NULL_VALUE = pyp.Literal("NULL")

VALUE = pyp.Or([NUMBER_VALUE, STR_VALUE, NULL_VALUE])
VALUES = pyp.Group(pyp.delimitedList(VALUE, ",")).setResultsName('rowvalues')
ROW = pyp.Group(("(" + VALUES + ")"))
ROWS = pyp.delimitedList(ROW, ',').setResultsName('rows')
TABLE_NAME = pyp.QuotedString("`").setResultsName("table")

INSERT = "INSERT INTO " + TABLE_NAME + "VALUES" + ROWS + ";"

def test():
  """Test parsing. Invoke using doctest.

  Test execution:
  >>> test()
  """
  # Basic sanity checks
  VALUE.parseString("'this is a string'")
  VALUE.parseString("'349384324349833'")
  VALUES.parseString("'340932403ererrwre93','34098439342'")
  ROW.parseString("('330984304983409832049823432432','34340983402984')")
  VALUES.parseString("1,2,'hello',4")
  ROWS.parseString("(1,2,3,4), (5,6,7,8)")
  INSERT.parseString('INSERT INTO `mytable` VALUES (1,2,3);')
  INSERT.parseString('INSERT INTO `mytable` VALUES (1,2,3),(4,5,6);')
  INSERT.parseString("INSERT INTO `anothertable` VALUES ('1210392039820398210938');")
  INSERT.parseString("INSERT INTO `anothertable` VALUES ('230918320938201938201','2039320938012983');")

  # Potential file based sanity checks
  #INSERT.parseString(open('exampledump.sql').read())

def parse_rows(f):
  s = ""
  for line in f:
    # Building up `s` until it is parseable. This is an ugly hack to be able to
    # parse multi-line dumps without having to read the whole dump content into
    # memory.
    s += line
    try:
      res = INSERT.parseString(s)
      for i, row in enumerate(res.rows):
        yield row.rowvalues
    except pyp.ParseException:
      pass
    else:
      s = ""

def run(f):
  writer = csv.writer(sys.stdout)
  for row in parse_rows(f):
    writer.writerow(row)

def main():
  if len(sys.argv) != 2:
    print "Usage: ./sqlparser.py <-|filename>"
    sys.exit(2)

  if sys.argv[1]=='-':
    f = sys.stdin
  else:
    f = open(sys.argv[1])

  with contextlib.closing(f):
    run(f)

if __name__ == '__main__':
  main()
