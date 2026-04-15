import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Designing Useful AI Agents',
  tagline: 'From Q&A to Real Business Impact with ADK and Twilio',
  favicon: 'img/favicon.ico',

  url: 'https://matos-workshop.vercel.app',
  baseUrl: '/',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true,
    faster: true,
  },

  onBrokenLinks: 'throw',
  markdown: {
    format: 'md',
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/', // Serve docs at root
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: '',
      logo: {
        alt: 'Build with AI Logo',
        src: 'img/bwai-logo-2026.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'right',
          label: 'Workshop Guide',
        },
      ],
    },
    footer: {
      style: 'light',
      links: [
        {
          title: 'Resources',
          items: [
            {
              label: 'Google ADK Docs',
              href: 'https://google.github.io/adk-docs/',
            },
            {
              label: 'Twilio Conversations',
              href: 'https://www.twilio.com/docs/whatsapp',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Build with AI Workshop.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'typescript', 'python', 'json'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
