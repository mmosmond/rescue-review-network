set terminal postscript eps enhanced color size 8cm, 16.0cm lw 1.6 font "Arial, 14"
set output "Figure_extinction.eps"

set style line 1 lt rgb "#0C7BDC" lw 1.6 dt 2
set style line 2 lt rgb "#FFC20A" lw 1.6 dt 4
set style line 3 lt rgb "#D41159" lw 1.6 dt 1



set encoding iso_8859_1
set macros

LEFTSPACE=1.5/8.0
BOTTOMSPACE=0.9/16.0
SIDESPACEX=0.5/8.0
SIDESPACEY=0.3/16.0
DELTAY=0.65/16.0

SIZEX=1-LEFTSPACE-SIDESPACEX
SIZEY=1./4.*(1-BOTTOMSPACE-3*DELTAY-SIDESPACEY)

LEFT = "set lmargin at screen LEFTSPACE; set rmargin at screen LEFTSPACE+SIZEX"

TOP = "set tmargin at screen BOTTOMSPACE+4*SIZEY+3*DELTAY; set bmargin at screen BOTTOMSPACE+3*DELTAY+3*SIZEY"
MIDDLE1 = "set tmargin at screen BOTTOMSPACE+3*SIZEY+2*DELTAY; set bmargin at screen BOTTOMSPACE+2*DELTAY+2*SIZEY"
MIDDLE2 = "set tmargin at screen BOTTOMSPACE+2*SIZEY+DELTAY; set bmargin at screen BOTTOMSPACE+DELTAY+SIZEY"
BOTTOM = "set tmargin at screen BOTTOMSPACE+SIZEY; set bmargin at screen BOTTOMSPACE"



set samples 1001
set multiplot layout 1,4


set xrange [0:400]
set xtics 0,100,400

set yrange [0:1]
set ytics 0,0.2,1.0


################## parameters ###############

d=1.0       #death rate; equal for all types

N0=10000    #total population size

################## wild-type parameters and functions, equal for all graphs ####################

r=0.08	    #decay rate

b_w=d-r	    #birth rate

# per-capita extinction times of a wild-type individual

Pw(x) = (d*exp(-(b_w-d)*x)-d)/(d*exp(-(b_w-d)*x)-b_w)

# distribution of extinction times of a pure wild-type population

Pwpop(x) = Pw(x)**(N0)



########## pre-existing mutant with p0=0.01 ############################

w0=9900	    #initial number of wild-type individuals
 
m0=N0-w0    #initial number of mutant individuals


######### supercritical mutant ############################

s_super=0.09		#growth advantage 

b_super=b_w+s_super  	#birth rate

# distribution of extinction times of a supercritical mutant individual

Psuper(x) = (d*exp(-(b_super-d)*x)-d)/(d*exp(-(b_super-d)*x)-b_super)

# distribution of extinction times of a population that contains m0 supercritical mutants

Psuperpop(x) = Pw(x)**w0*Psuper(x)**m0

Prescue=1-(d/b_super)**m0


######### subcritical mutant ################################

s_sub=0.07		#growth advantage

b_sub=b_w+s_sub		#birht rate

# distribution of extinction times of a subcritical mutant

Psub(x) = (d*exp(-(b_sub-d)*x)-d)/(d*exp(-(b_sub-d)*x)-b_sub)

# distribution of extinction times of a population that contains m0 subcritical mutants

Psubpop(x) = Pw(x)**w0*Psub(x)**m0


########## Graphs ####################

@LEFT;@TOP
set label "a" at -70,1 font "{Arial-Bold}"

set key reverse invert Left font "Arial, 16"
set key left at 160,0.57 
set key samplen 1.35
set key spacing 1.25

set xtics format ""
set arrow nohead from 73.15,0 to 73.15,1 lw 1.4 lc rgb "#A9A9A9" dt 3


set ylabel "{/Arial_Italic P(T}@_{ext}&{ex} > {/Arial_Italic t)}" font "Arial, 18"


plot 1-Pwpop(x) ls 1 title "wild-type population", 1-Psubpop(x) ls 2 title "subcritical mutant", 1-Psuperpop(x) ls 3 title "supercritical mutant", Prescue lw 1.4 dt 3 lc rgb "#A9A9A9" notitle


set nokey

@LEFT;@MIDDLE1
unset label
set label "b" at -70,1 font "{Arial-Bold}"


set ylabel "{/Arial_Italic P}_{rescue}(t)" offset 0.05,0 font "Arial, 18"


plot 1-(Psub(x)/Pw(x))**m0 ls 2 title "subcritical mutant", 1-(Psuper(x)/Pw(x))**m0 ls 3 title "supercritical mutant",  Prescue lw 1.4 dt 3 lc rgb "#A9A9A9" notitle



@LEFT;@MIDDLE2
unset label
set label "c" at -70,1 font "{Arial-Bold}"


set ylabel "{/Symbol D}{/Arial_Italic P}(t)" offset 0.05,0 font "Arial, 18"


plot (1-Psubpop(x))-(1-Pwpop(x)) ls 2 title "subcritical mutant", (1-Psuperpop(x))-(1-Pwpop(x)) ls 3 title "supercritical mutant", Prescue lw 1.4 dt 3 lc rgb "#A9A9A9" notitle



@LEFT;@BOTTOM
unset label
set label "d" at -70,1 font "{Arial-Bold}"

set xtics format "%g"

set xlabel "time {/Arial t}" font "Arial, 18"
set ylabel "{/Arial_Italic P}_{evo-survival}(t)" offset 0.05,0 font "Arial, 18"



plot (1.-Psubpop(x)-1.+Pwpop(x))/(1.-Psubpop(x)) ls 2 title "subcritical mutant", (1.-Psuperpop(x)-1.+Pwpop(x))/(1-Psuperpop(x)) ls 3 title "supercritical mutant"


#### small plot

reset
set style line 1 lt rgb "#0C7BDC" lw 1.5 dt 2
set style line 2 lt rgb "#FFC20A" lw 1.5 dt 4
set style line 3 lt rgb "#D41159" lw 1.5 dt 1



set samples 10001
set border lw 0.5
set size 0.36, 0.12
set origin 0.58, 0.06+2*SIZEY+2*DELTAY

set xrange [0:10]
set yrange [0:1]

set xtics 0,5,10 font "Arial, 12" offset 0,0.4
set ytics 0,1 font "Arial, 12" offset 0.4,0



plot 1-(Psub(x)/Pw(x))**m0 ls 2 notitle, 1-(Psuper(x)/Pw(x))**m0 ls 3 notitle




unset multiplot
reset
set term wxt
set output



