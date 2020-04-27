#!/usr/bin/perl -w
use strict;
use warnings;

my $file = "./result.ssv";
open(FILE, "<", $file) or die "$!";

my $p0 = 0;
my $p1 = 0;

while(<FILE>){
  if(!($_ =~ /^#/)){
    $_ =~ /([01])[01]+\s+(.+)/;
    if($1 == 0){
      $p0 = $p0 + $2;
    }
    else{
      $p1 = $p1 + $2;
    }
  }
}

print("# qubit(c_bob) probability \n");
print("0 $p0\n");
print("1 $p1\n");
