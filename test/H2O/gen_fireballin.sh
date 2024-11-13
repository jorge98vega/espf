run=$1
iwrtxsf=$2
Ecut=$3
iqout=$4
mol=$5

charge="${mol//[^-]}"

cat << EOF > fireball.in
&OPTION
fdatalocation = "/home/jorge/research/charges/runs/${run}/Fdata"
nstepf = 1
iquench = -1
icluster = 1
iqout = $iqout
qstate = ${#charge}
dt = 0.5
idipole = 1
iks = 1
imcweda = 0
idogs = 0
bmix = 0.04
verbosity = 1
&END
&OUTPUT
iwrtxyz = 1
iwrtdipole = 2
iwrtcharges = 4
iwrtxsf = $iwrtxsf
&END
&MESH
Ecut = $Ecut ! points in each grid directon with icluster = 1: ~ Ecut * avec
droff = 1.0d0
&END
EOF
