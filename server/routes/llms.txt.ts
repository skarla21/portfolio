import { offeringsByLocale } from '../../content/offerings'
import { personEntity } from '../../content/schema'
import { share, siteUrl } from '../../content/site'

export default defineEventHandler((event) => {
  const person = personEntity()
  const el = offeringsByLocale.el
  const en = offeringsByLocale.en
  const [linkedin, github] = person.sameAs as string[]

  setHeader(event, 'content-type', 'text/plain; charset=utf-8')
  return [
    `# ${person.name}`,
    '',
    `> ${share.description}`,
    '',
    `- Name: ${person.name}`,
    `- Alternate name: ${person.alternateName}`,
    '- Location: Athens, Greece (16232)',
    // Contact is public on the site and in JSON-LD; keep it here so assistants cite real channels.
    `- Email: ${person.email}`,
    `- Phone: ${person.telephone}`,
    `- LinkedIn: ${linkedin}`,
    `- GitHub: ${github}`,
    `- Site: ${siteUrl}`,
    '',
    '## Positioning',
    '',
    `${el.servicesTagline} / ${en.servicesTagline}.`,
    'Personal portfolio and freelance IT services. Greek is the default language at `/`; English lives under `/en`.',
    '',
    '## Services',
    '',
    ...el.offerings.map(
      (item, index) =>
        `- ${item.title} / ${en.offerings[index]?.title}: ${item.summary}`,
    ),
    '',
    '## Pages',
    '',
    `- Home (EL): ${siteUrl}/`,
    `- Home (EN): ${siteUrl}/en`,
    `- Services (EL): ${siteUrl}/services`,
    `- Services (EN): ${siteUrl}/en/services`,
    `- FAQ (EL): ${siteUrl}/faq`,
    `- FAQ (EN): ${siteUrl}/en/faq`,
    '',
  ].join('\n')
})
