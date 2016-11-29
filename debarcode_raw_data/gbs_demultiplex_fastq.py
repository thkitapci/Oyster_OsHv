#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to demultiplex fastq.gz files

This program uses the barcode sequences, stored in a file, to demultiplex
a fastq.gz file. One file is created per individual and other for the un-
matched sequences

Args:
  file: fastq.gz file
  barcodes: file with barcode sequence for each individual and library
  output_folder: folder to output one fastq file for each barcode

Return:
  void
"""
# modulo do sistema
# TODO: Add command line argument for the file we have to process
# ADD lines for creating and checking an output directory

# Remove prints
# Check the lines where reads are saved!!!!
import sys
import gzip
import os
import argparse

# from Bio.Seq import Seq
# from Bio.Alphabet import IUPAC

"""
my_seq = Seq("AATTC", IUPAC.unambiguous_dna)
my_seq[::-1]
str(my_seq[::-1])

check
Fuzzy matching
http://stackoverflow.com/questions/15524822/how-to-find-a-imperfect-substring
https://pypi.python.org/pypi/regex/
"""



class Record:
  """A class to hold data about a read"""
  def __init__(self, name, sequence, quality):
    self.name = name
    self.sequence = sequence
    self.plus = '+\n'
    self.quality = quality

  def clean_record(self, bc_length):
    self.sequence = self.sequence[bc_length:]
    self.quality = self.quality[bc_length:]

  def join_record(self):
    return "".join([self.name, self.sequence, self.plus, self.quality])

  def clean_record_end(self,position):
    self.sequence = self.sequence[:position+4] + "\n"
    self.quality = self.quality[:position+4] + "\n"

class Barcode:
  """"A class to hold barcode data"""
  def __init__(self, library, sequence, individual):
    self.library = library
    self.sequence = sequence
    self.individual = individual
    self.length = len(sequence)
    self.w_cut_site = sequence + 'AATT'
    self.len_wcs = len(sequence) + 4

    self.isequence = self.sequence[::-1]
    tmp_seq = []
    for i in self.isequence:
      if i == "A":
        tmp_seq.append('T')
      elif i == "C":
        tmp_seq.append('G')
      elif i == "G":
        tmp_seq.append('C')
      elif i == "T":
        tmp_seq.append('A')
    self.isequence = ''.join(tmp_seq)
  def file_name(self):
    file_name = "-".join([self.individual, self.sequence, self.library])
    return '{0}.fastq'.format(file_name)
  def file_nameR1(self):
    file_name = "-".join([self.individual, self.sequence, self.library])
    return '{0}_R1.fastq'.format(file_name)
  def file_nameR2(self):
    file_name = "-".join([self.individual, self.sequence, self.library])
    return '{0}_R2.fastq'.format(file_name)
    
def process_command_line():
  """
  Parse the command line options
  """
  parser = argparse.ArgumentParser(description = (
      "Program to demultiplex fastq.gz files"
      ), prog = 'gbs_demultiplex_fastq.py'
                                   )
  parser.add_argument("file",
                      help = "fastq.gz file")
  parser.add_argument("barcodes",
                      help = (
                        "file with barcode information. Fields in this order:"
                        " file.fastq.gz library barcode individual_name")
  )
  parser.add_argument("output_folder",
                      help = 'folder where output files will be stored')
  parser.add_argument("--read2", default = None,
                      help = (
                        'second reads file'
                      )
                    )
  # parser.add_argument('--version', action='version',
  #                     version = ('%(prog)s gatk 3.1-1'))
  args = parser.parse_args()
  return args
    
def read_barcodes(library, file_barcodes):
  """
  Function to read barcode information
  
  Input: a file with the following information (file_name, library_name, barcode
  and individual name. Example:
  0072_exp_qual_c-20121006-D-snp1113.fastq.gz	0072	AACT	51x35_043_m

  This function also uses library argument, only barcodes pertinent to a
  library are kept

  Output: a list of lists with the previous information
  """
  fin = open(file_barcodes, 'rU')
  barcodes = fin.readlines()
  barcodes = [i.split() for i in barcodes]

  # Loop to keep only barcodes relevant to the file
  # Temporal variable to hold barcode and associated information
  barcode_bak = []
  # Go through list of list. If the barcodes correspond to the current file keep
  # the library name, the barcode and the individual name.
  for i in xrange(len(barcodes)):
    barcode = barcodes[i]
    if barcode:
      if barcode[0] == library:
        i = Barcode(barcode[1], barcode[2], barcode[3])
        barcode_bak.append(i)
  
  # for barcode in barcodes:
  #   if barcode[0] == library:
  #     barcode_bak.append((barcode[1], barcode[2], barcode[3]))

  barcodes = barcode_bak
  # Remove temporal variable
  del barcode_bak

  return barcodes

  # Loop to keep only barcodes relevant to the file
  # Temporal variable to hold barcode and associated information
  barcode_bak = []
  # Go through list of list. If the barcodes correspond to the current file keep
  # the library name, the barcode and the individual name.
  for barcode in barcodes:
    if barcode[0] == file_name:
      barcode_bak.append((barcode[1], barcode[2], barcode[3]))

  barcodes = barcode_bak
  # Remove temporal variable
  del barcode_bak


def search_seq_2nd_read(seq1, seq2, barcode):
  """
  Function to search in the second read of a pair the remnant site

  Input:
    Two strings. seq1: read, seq2: remnant
    barcode
  Return:
    Position if remnant site was found
    0 if not
  """
  l1 = len(seq1)
  l2 = len(seq2)

  if l2 > l1:
    print "seq1 has to be longer than seq2"
    sys.exit(1)
  # Number comparisons between seq1 and seq2
  num_comp = l1 - l2 + 1
  # Create a list with the positions to compare
  # This goes from minus the length of the remnant site (seq2) to position
  # minus length of sequence plus four (i.e. we do not consider the initial AATT
  # because it can not be the beginning and the end at the same time
  pos = xrange(-(l1 - num_comp + 1), -l1 + 4, -1)

  for i in pos:
    j = i + l2
    if j == 0:
      seq_tmp = seq1[i:]
      # If the sequence selected is shorter than three skip searching for the
      # remnant site
      if len(seq_tmp) < 3:
        return 0
      # If we find remnant site
      if dif_between_seqs(seq_tmp, seq2):
        if comp_tail_barcode(seq1, barcode, i):
          return i
    if j != 0:
      seq_tmp = seq1[i:j]
      if len(seq_tmp) < 3:
        return 0
      if dif_between_seqs(seq_tmp, seq2):
        if comp_tail_barcode(seq1, barcode, i):
          return i
  return 0

def comp_tail_barcode(seq, barcode, position):
  """
  Function to compare the tail and the barcode.
  Tail: sequence after remnant site in the second read of a
  paired end

  Args:
    seq: sequence where remnant site was found
    barcode: barcode instance
    position: position where remnant site begins

  Return:
    boolean: tail matches barcode sequence
  """
  # Tail: sequence after remnant site (which has a fixed length of 5).
  tail = seq[position + 5:]
  
  # If there is no sequence after the remnant site
  if not tail:
    return True
  # If the sequence after remnant site is shorter than
  # barcode cut the barcode to the apropiate size
  if len(tail) < barcode.length:
    subset_bc = barcode.isequence[:len(tail)]
    if tail == subset_bc:
      return True
    elif dif_between_seqs(tail, subset_bc):
      return True
  # If tail sequence has the same length than barcode
  elif len(tail) == barcode.length:
    if dif_between_seqs(tail, barcode.isequence):
      return True
  # If tail is longer than barcode, cut tail to barcode length
  elif len(tail) > barcode.length:
    tail = tail[:barcode.length]
    if dif_between_seqs(tail, barcode.isequence):
      return True
  return False



def dif_between_seqs(seq1, seq2):
  """
  Function to compare two sequences. If they differ by more than one position return false.

  Input: two sequences

  Output: Return True (the sequences have a maximum of 1 differences) or False
  (the sequences have more than one difference)
  """

  # Var to hold the number of differences
  differences = 0
  # Go through sequence positions
  for i in xrange(len(seq1)):
    # If positions differ increment variable
    if seq1[i] != seq2[i]:
      differences += 1
    # If differences are bigger than one return False
    if differences > 1:
      return False
  return True

def common_adap(read):
  """
  Function to check for full cut site (from partial digest or chimera) or
  common adapter start
  """
  possible_read_end = ['AAATTAGAT', 'GAATTAGAT', 'AAATTC', 'AAATTT', 'GAATTC', 'GAATTT']

  for end in possible_read_end:
    pos = read.sequence.find(end)
    if pos != -1:
      read.clean_record_end(pos)
      break

def perfect_barcode(barcodes, read):
  """
  Function to check if the sequence of the barcode matches perfectly
  in the sequence
  INPUT: read, barcodes
  OUTPUT:
    'clean' sequence,
    barcode sequence (to know in which file save the read)
    boolean: 0 barcode found, 1 barcode not found
    barcode: barcode instance
  """

  remnant = ['AATTC', 'AATTT']
  
  # Go through barcodes
  for barcode in barcodes:
    # Part of the fastq sequence we are going to compare
    seq_beg = read.sequence[:barcode.length]
    # Check if there is a perfect match
    if barcode.sequence == seq_beg:
      # Check if there is a perfect match with the remnant cut site
      after_bc = read.sequence[barcode.length : (barcode.length + 5)]
      if after_bc in remnant:
        read.clean_record(barcode.length)
        common_adap(read)
        return (read, barcode.sequence, 0, barcode)
      # Check if there is an imperfect match with the remnant cut site
      else:
        if dif_between_seqs(after_bc, remnant[0]):
          read.clean_record(barcode.length)
          common_adap(read)
          return (read, barcode.sequence, 0, barcode)
        elif dif_between_seqs(after_bc, remnant[1]):
          read.clean_record(barcode.length)
          common_adap(read)
          return (read, barcode.sequence, 0, barcode)
    # Check if there is an imperfect match with the barcode
    elif dif_between_seqs(barcode.sequence, seq_beg):
      # Check if there is a perfect match with the remnant cut site
      after_bc = read.sequence[barcode.length : (barcode.length + 5)]
      if after_bc in remnant:
        read.clean_record(barcode.length)
        common_adap(read)
        return (read, barcode.sequence, 0, barcode)
      # Check if there is an imperfect match with the remnant cut site
      else:
        if dif_between_seqs(after_bc, remnant[0]):
          read.clean_record(barcode.length)
          common_adap(read)
          return (read, barcode.sequence, 0, barcode)
        elif dif_between_seqs(after_bc, remnant[1]):
          read.clean_record(barcode.length)
          common_adap(read)
          return (read, barcode.sequence, 0, barcode)
  return (read, "", 1, barcode)

  # # First round: perfect barcodes
  # for barcode in barcodes:
  #   # Part of the fastq sequence we are going to compare
  #   seq_beg = read.sequence[:barcode.length]
  #   # TRY the startwith()
  #   if barcode.sequence == seq_beg:
  #     if read.sequence[barcode.length : barcode.len_wcs] == 'AATT':
  #       read.clean_record(barcode.length)
  #       common_adap(read)
  #       return (read, barcode.sequence, 0)
  #   # This return was preventing finding reads with imperfect barcodes
  #   # when this imperfect barcode had part of its sequence equal to a 
  #   # good barcode
  #     # else:
  #     #   return (read, "", 1)

  # # Second round: imperfect barcodes
  # for barcode in barcodes:
  #   # Check first if there is the remnant site
  #   if read.sequence[barcode.length : barcode.len_wcs] == 'AATT':
  #     seq_beg = read.sequence[:barcode.length]

  #     if dif_between_seqs(barcode.sequence, seq_beg):
  #       read.clean_record(barcode.length)
  #       common_adap(read)
  #       return (read, barcode.sequence, 0)

  #   # Do not require the remnant site to be perfect
  #   seq_beg = read.sequence[:barcode.len_wcs]
  #   if dif_between_seqs(barcode.w_cut_site, seq_beg):
  #     read.clean_record(barcode.length)
  #     common_adap(read)
  #     return (read, barcode.sequence, 0)

  # return (read, "", 1)
  # print "Problems with the perfect_barcode() function"
  # sys.exit(1)

def main(argv=None):
  # Read command line arguments
  args = process_command_line()
  file_name = args.file
  dir_out = args.output_folder
  file_barcodes = args.barcodes

  # check that the output directory exists
  if not os.path.exists(dir_out):
    print "the output folder does not exist"
    sys.exit(1)

  dir_out = os.path.abspath(dir_out)

  # Read barcodes
  barcodes = read_barcodes(file_name, file_barcodes)
  if not barcodes:
    print "The fastq.gz file was not found in the barcode file"
    sys.exit(1)

  # Create the file where unmatched sequences will be stored
  unmatched_files = 'unmatched-%s.fastq' % barcodes[0].library
  unmatched_files = os.path.join(dir_out, unmatched_files)
  unmatched = open(unmatched_files, "w")

  # Counter to follow the number of sequences inspected
  num = 1
  # Open file with sequences
  handle_in = gzip.open(file_name, 'r')
  # Open file with read2
  if args.read2:
    handle_in2 = gzip.open(args.read2, 'r')

  # Go trough sequences
  # If we have paired data create two dictionaries
  if args.read2:
    files_dictR1 = {}
    files_dictR2 = {}
  else:
    files_dict = {}

  for barcode in barcodes:
    # If we have paired data go throuh both files
    if args.read2:
      handle_out1 = os.path.join(dir_out, barcode.file_nameR1())
      handle_out2 = os.path.join(dir_out, barcode.file_nameR2())
      files_dictR1[barcode.sequence] = open(handle_out1, "w")
      files_dictR2[barcode.sequence] = open(handle_out2, "w")
    else:
      handle_out = os.path.join(dir_out, barcode.file_name())
      files_dict[barcode.sequence] = open(handle_out, "w")

  # Read lines until end of file
  # First line is the name, then we have the sequence, optional information
  # and the quality
  while True:
    name = handle_in.readline()
    if name == '':
      break
    sequence = handle_in.readline()
    handle_in.readline()
    quality = handle_in.readline()

    # The same for the second read
    if args.read2:
      name2 = handle_in2.readline()
      sequence2 = handle_in2.readline()
      handle_in2.readline()
      quality2 = handle_in2.readline()
      read2 = Record(name2, sequence2, quality2)

    # Every million sequences print the number of sequences examined
    if not (num % 1000000):
      print num
    num += 1

    # Create a Record instance and check for the barcode
    read = Record(name, sequence, quality)
    read, file_name, flag, barcode = perfect_barcode(barcodes, read)

    if flag == 0:
      if args.read2:
        files_dictR1[file_name].write(read.join_record())
        read2_clean = False
        for i in ['AAATT', 'GAATT']:
          position = search_seq_2nd_read(read2.sequence.rstrip(), i, barcode)
          if position:
            read2.clean_record_end(position)
            files_dictR2[file_name].write(read2.join_record())
            read2_clean = True
            break
        if not read2_clean:
          files_dictR2[file_name].write(read2.join_record())
      else:
        files_dict[file_name].write(read.join_record())
    else:
      unmatched.write(read.join_record())
  return 0
if __name__ == '__main__':
  status = main()
  sys.exit(status)
  main()
