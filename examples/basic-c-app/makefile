SHELL = /bin/bash

OUTDIR = Output
BUILDDIR = Build

OUTFILE = $(OUTDIR)/basicapp

OBJS = \
	$(BUILDDIR)/main.o \
	$(BUILDDIR)/module1.o \

CC = gcc

CFLAGS = -O3 -Wall -std=c99

.PHONY:				all
all:				$(OUTFILE) removebuild

$(OUTFILE): 		$(OBJS) $(OUTDIR)
					@$(CC) $(CFLAGS) $(OBJS) -o $@

$(BUILDDIR)/%.o:	%.c $(BUILDDIR)
					@$(CC) -c $(CFLAGS) $< -o $@

$(BUILDDIR):
					@mkdir "$(BUILDDIR)"

$(OUTDIR):
					@mkdir "$(OUTDIR)"

.PHONY:				removebuild
removebuild:
					@if [ -d "$(BUILDDIR)" ]; then rm -r "$(BUILDDIR)"; fi;

.PHONY:				run
run:				all
					@chmod +x $(OUTFILE); \
					./$(OUTFILE);

.PHONY:				clean
clean:
					@if [ -d "$(OUTDIR)" ]; then rm -r "$(OUTDIR)"; fi;
