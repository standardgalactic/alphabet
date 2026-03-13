for f in nova sga cursive
do
  lualatex -jobname=geodesics-$f "\def\fontvariant{$f}\input{font-test-02.tex}"
done
