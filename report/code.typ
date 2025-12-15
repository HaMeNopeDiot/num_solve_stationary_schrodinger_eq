#import "@preview/codelst:2.0.2": sourcecode

#let codeblock(body, caption: none, lineNum:false) = {
    if lineNum {
      show raw.where(block:true): it =>{
        set par(justify: false)
        block(fill: luma(240),inset: 0.3em,radius: 0.3em, 
          // grid size: N*2
          grid(
            columns: 2,
            align: left+top,
            column-gutter: 0.5em,
            stroke: (x,y) => if x==0 {( right: (paint:gray, dash:"densely-dashed") )},
            inset: 0.3em,
            ..it.lines.map((line) => (str(line.number), line.body)).flatten()
          )
        )
      }
      figure(body, caption: caption, kind: "code", supplement: "Code")
    }
    else{
      figure(body, caption: caption, kind: "code", supplement: "Code")
    }
  }

= Приложение 1. Компьютерный код

Листинг файла main.py
#let main_code = read("main.py")
#sourcecode(
    lang: "python",
    frame: codeblock,
)[
    #raw(main_code)
]

Листинг файла qma.py
#let qma_code = read("qma.py")
#sourcecode(
    lang: "python",
    frame: codeblock
)[
    #raw(qma_code)
]