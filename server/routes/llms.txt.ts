import { profilePage, share, siteUrl } from '../../content/site'

export default defineEventHandler((event) => {
  const person = profilePage.mainEntity
  const [linkedin, github] = person.sameAs

  setHeader(event, 'content-type', 'text/plain; charset=utf-8')
  return [
    `# ${person.name}`,
    '',
    `> ${share.description}`,
    '',
    `- Name: ${person.name}`,
    `- Alternate name: ${person.alternateName}`,
    '- Location: Athens, Greece',
    `- Current role: ${person.jobTitle[0]} at ${person.worksFor.name}`,
    `- Site: ${siteUrl}`,
    `- LinkedIn: ${linkedin}`,
    `- GitHub: ${github}`,
    '',
    'Personal portfolio. One page, Greek by default, with an English toggle.',
    '',
  ].join('\n')
})
