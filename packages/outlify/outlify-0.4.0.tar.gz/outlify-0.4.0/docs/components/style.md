# Styles

The **Style** module allows you to customize text styling and colors,
including in **Outlify** elements.

To view the demo for the **Panel** module use:

```sh
python -m outlify.style
```

## `Colors`
A class for managing text colors.

### Available fields

| Field     |   Value    | Comments                               |
|-----------|:----------:|----------------------------------------|
| `black`   | `\033[30m` |
| `red`     | `\033[31m` |
| `green`   | `\033[32m` |
| `yellow`  | `\033[33m` |
| `blue`    | `\033[34m` |
| `magenta` | `\033[35m` |
| `cyan`    | `\033[36m` |
| `white`   | `\033[37m` |
| `default` | `\033[39m` |
| `gray`    | `\033[90m` |
| `reset`   | `\033[0m`  | reset all styles include colors/styles |

## `Styles`
A class for managing text styles.

### Available fields

| Fields        |   Value    | Comments                               |
|---------------|:----------:|----------------------------------------|
| `bold`        | `\033[1m`  |
| `dim`         | `\033[2m`  |
| `italic`      | `\033[3m`  |
| `underline`   | `\033[4m`  |
| `crossed_out` | `\033[9m`  |
| `default`     | `\033[22m` |
| `reset`       | `\033[0m`  | reset all styles include colors/styles |


## Advanced
### Ansi escape sequences

!!! question

    Why are pre-prepared ansi escape sequences for each style used separately instead of together?
    (`\033[1m\033[30m` instead of `\033[1;30m`)

The difference between terminal processing of the first and second variants
is very small. If we make a convenient class that will process and create
one sequence of ansi characters, it will take more time to process it than
separate ones. Convenience is chosen over hundred-thousandths of a second
of execution time.

To check the processing time of these two options, you can run this code:

```python
from time import time

def timer(text: str):
    now = time()
    print(text)
    return time() - now

timer('warp up')
x = timer('\033[31m\033[1m\033[0m')
y = timer('\033[31;1m\033[0m')

print('Results:')
print(f'1. single ansi escape sequence: {x:10f}')
print(f'2. multiple ansi escape sequence: {y:10f}')
print(f'{x / y:2f} times faster')
```

<div class="result" markdown>

```
warp up


Results:
1. single ansi escape sequence:   0.000003
2. multiple ansi escape sequence:   0.000003
1.166667 times faster
```

</div>