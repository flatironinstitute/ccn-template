r"""
# Example LaTeX Equations

Thanks to the [KaTeX](https://katex.org/) library, you can display equations efficiently in any browser.

## Inline Equations

You can write LaTeX inline equations by enclosing them in `$` symbols or between round parentheses `\\\( ... \\\)`.

Here are two examples: $E = mc^2$ and \\(e^{i \pi} + 1 = 0\\).

!!! notes
    If you inspect this script, you can note that the module-level docstring is in raw string format
    (starts with `r`),  which is necessary for correct parsing of parentheses.
"""
import cmath

euler_formula = "exp(i\u00B7\u03C0) + 1"
result = cmath.e**(cmath.pi * 1j) + 1

print(f"{euler_formula} = {result.real:.2f} + i{result.imag:.2f}")

# %%
# ##  Block Equations
#
# Block equations can be enclosed by either double `$` symbols or squared parentheses `\\\[ ... \\\]`. For example:
#
# $$ E = m c^2, $$
# Or
# \\[
# e^{i \pi} + 1  = 0.
# \\]

