# Copyright 2020 by mars

# Description: Makefile for building a branch predictor.
#


LDFLAGS += 

LDLIBS   += -lz

CPPFLAGS := -O3 -Wall -Wextra -Winline -Winit-self -Wno-sequence-point\
           -Wno-unused-function -Wno-inline -fPIC -W -Wcast-qual -Wpointer-arith

PROGRAMS := predictor

objects = bt9.o main.o predictor.o

all: $(PROGRAMS)

predictor : $(objects)
	gcc $(CPPFLAGS) $(LDFLAGS) -o $@ $^ $(LDLIBS)
	rm -f $(objects)

clean:
	rm -f $(PROGRAMS) $(objects)
