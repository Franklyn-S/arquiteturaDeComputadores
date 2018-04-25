const getRandomRanges = (ranges = 1) => {
  let classes = Array(ranges);
  let offset = Math.random() * (359 / ranges);
  for (let i = 0; i < ranges; i++) {
    classes[i] = Math.floor(offset + (359 / ranges) * i)
  }
  return classes.sort((a, b) => Math.random() - Math.random()).map(h => {
    let s = Math.floor(Math.random() * 50) + 20;
    let l = Math.floor(Math.random() * 50) + 20;
    return [h, l, s];
  });
}

getRandomRanges(20).forEach(([h, s, l]) => {
  document.body.innerHTML += `
  	<div class="square" style="background-color: hsl(${h}, ${s}%, ${l}%)" >
    </div.
  `;
});

/*


print('{} | {} | {}'.format('{:^14s}'.format('LABEL'), '{:^14s}'.format('MNEMONIC'), '{:^14s}'.format('ARGUMENT')))
print('{} | {} | {}'.format('{:^14s}'.format('-'), '{:^14s}'.format('-'), '{:^14s}'.format('-')))

print(
    "\n".join(
        list(
            map(
                lambda x: 
                " | ".join(
                    list(
                        map(
                            lambda y: '{:^14s}'.format(y),
                            x
                        )
                    )
                ),
                cmds
            )
        )
    )
)

*/