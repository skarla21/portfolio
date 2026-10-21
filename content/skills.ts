import {
  siC,
  siCss,
  siExpress,
  siGit,
  siGnubash,
  siHtml5,
  siJavascript,
  siLinux,
  siMongodb,
  siMysql,
  siNextdotjs,
  siNodedotjs,
  siNuxt,
  siOpenjdk,
  siPython,
  siReact,
  siTypescript,
  siVite,
  siVuedotjs,
  siWebpack,
  type SimpleIcon,
} from 'simple-icons'

export type SkillMark = {
  title: string
  path?: string
  letters?: string
  hex: string
}

function fromIcon(title: string, icon: SimpleIcon): SkillMark {
  return { title, path: icon.path, hex: icon.hex }
}

export const skills: SkillMark[] = [
  fromIcon('JavaScript', siJavascript),
  fromIcon('TypeScript', siTypescript),
  fromIcon('HTML', siHtml5),
  fromIcon('CSS', siCss),
  fromIcon('Python', siPython),
  { title: 'SQL', letters: 'SQL', hex: '336791' },
  fromIcon('Java', siOpenjdk),
  fromIcon('Bash', siGnubash),
  fromIcon('C', siC),
  fromIcon('React', siReact),
  fromIcon('Next.js', siNextdotjs),
  fromIcon('Vue', siVuedotjs),
  fromIcon('Nuxt', siNuxt),
  fromIcon('Node', siNodedotjs),
  fromIcon('Express', siExpress),
  fromIcon('Git', siGit),
  fromIcon('MySQL', siMysql),
  fromIcon('MongoDB', siMongodb),
  fromIcon('Vite', siVite),
  fromIcon('Webpack', siWebpack),
  fromIcon('Linux', siLinux),
  { title: 'Visual Studio Code', letters: 'VS', hex: '007ACC' },
]

export function markColor(hex: string) {
  const value = Number.parseInt(hex, 16)
  const red = (value >> 16) & 255
  const green = (value >> 8) & 255
  const blue = value & 255
  const luminance = (0.2126 * red + 0.7152 * green + 0.0722 * blue) / 255
  return luminance < 0.22 ? '#f3efe4' : `#${hex}`
}
