## Data Science

Five types of command line tools
* Binary Executable: compiled, cannot read
* Shell Builtin: cd, ls eg
* Interpreted Script: has shebang line to tell how to interpret
* shell function: `fac() { (echo 1; seq $1) | paste -s -d\* - | bc; }`
* alias

```bash
# number of numbers containing 3
seq 100 | grep 3 | wc -l

# no trailing newline
echo -n "Hello"

# check first 20 lines of manual
man cat | head -n 20
help cd | head -n 20
```

### Chapter 3
