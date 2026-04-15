import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'doc',
      id: 'env-vars',
      label: 'Variables d\'environnement',
    },
    {
      type: 'doc',
      id: 'setup',
      label: 'Configuration',
    },
    {
      type: 'doc',
      id: 'deploy-backend',
      label: 'Déployer le backend',
    },
    {
      type: 'doc',
      id: 'build-agent',
      label: 'Construire l\'agent',
    },
    {
      type: 'doc',
      id: 'deploy-agent',
      label: 'Déployer l\'agent',
    },
    {
      type: 'doc',
      id: 'build-bridge',
      label: 'Construire le pont WhatsApp',
    },
    {
      type: 'doc',
      id: 'deploy-bridge',
      label: 'Déployer le pont WhatsApp',
    },
    {
      type: 'doc',
      id: 'validation-and-troubleshooting',
      label: 'Validation et dépannage',
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
