import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { collectOperations } from './generate-resources.mjs';

const NODE_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function signature(operation, property) {
  if (operation.resource === 'chat') {
    return 'client.chat.completions.create(params)';
  }
  const params = operation.pathParams.map((param) => param.name);
  if (operation.kind === 'list') {
    params.push(operation.pathParams.length > 0 ? 'params?' : 'params?');
  } else if (['post', 'patch', 'put'].includes(operation.kind) && !operation.emptyBody) {
    params.push('body?');
  }
  if (operation.kind === 'custom' && operation.method === 'listenRequest') {
    params.push('options?');
  }
  return `client.${property}.${operation.method}(${params.join(', ')})`;
}

function generateApiDocs(resources) {
  const sections = resources
    .sort((left, right) => left.title.localeCompare(right.title))
    .map((resource) => {
      const operations = resource.operations
        .filter((operation) => operation.kind !== 'manual' || operation.resource === 'chat')
        .map((operation) => `- \`${signature(operation, resource.property)}\``)
        .join('\n');
      return `## ${resource.title}\n\n${operations}`;
    });

  return `# API Reference

## Client

- \`new Layerbrain(options?)\`

${sections.join('\n\n')}
`;
}

fs.writeFileSync(path.join(NODE_ROOT, 'api.md'), generateApiDocs(collectOperations()));
