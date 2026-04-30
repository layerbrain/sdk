# API Reference

## Client

- `new Layerbrain(options?)`

## 3D

- `client.threeD.generate(body?)`
- `client.threeD.retrieve(generationId)`

## Accounts

- `client.accounts.list(params?)`
- `client.accounts.delete(id)`
- `client.accounts.retrieve(id)`
- `client.accounts.update(id, body?)`

## API Keys

- `client.apiKeys.create(body?)`
- `client.apiKeys.list(params?)`
- `client.apiKeys.delete(id)`
- `client.apiKeys.update(id, body?)`
- `client.apiKeys.retrieve(id)`
- `client.apiKeys.rotate(id)`

## Audio

- `client.audio.speech(body?)`
- `client.audio.transcriptions(body?)`

## Brains

- `client.brains.create(body?)`
- `client.brains.delete(id)`
- `client.brains.retrieve(id)`
- `client.brains.archive(id)`

## Chat

- `client.chat.completions.create(params)`

## Compute

- `client.compute.list(params?)`
- `client.compute.retrieve(id)`

## Embeddings

- `client.embeddings.create(body?)`

## Images

- `client.images.edit(body?)`
- `client.images.generate(body?)`

## Machines

- `client.machines.create(body?)`
- `client.machines.list(params?)`
- `client.machines.delete(machineId)`
- `client.machines.retrieve(machineId)`
- `client.machines.connect(machineId)`
- `client.machines.extend(machineId, body?)`
- `client.machines.restore(machineId, body?)`
- `client.machines.snapshot(machineId, body?)`

## Memberships

- `client.memberships.create(body?)`
- `client.memberships.list(params?)`
- `client.memberships.retrieve(id)`

## Models

- `client.models.list(params?)`
- `client.models.retrieve(modelId)`

## Network Flows

- `client.networkFlows.list(params?)`
- `client.networkFlows.retrieve(id)`

## Network Rules

- `client.networkRules.create(body?)`
- `client.networkRules.list(params?)`
- `client.networkRules.delete(id)`
- `client.networkRules.update(id, body?)`
- `client.networkRules.retrieve(id)`

## Networks

- `client.networks.list(params?)`
- `client.networks.update(id, body?)`
- `client.networks.retrieve(id)`

## Organizations

- `client.organizations.create(body?)`
- `client.organizations.list(params?)`
- `client.organizations.delete(id)`
- `client.organizations.retrieve(id)`
- `client.organizations.update(id, body?)`

## Secrets

- `client.secrets.create(body?)`
- `client.secrets.list(params?)`
- `client.secrets.delete(id)`
- `client.secrets.update(id, body?)`
- `client.secrets.retrieve(id)`
- `client.secrets.reveal(id)`

## Snapshots

- `client.snapshots.create(body?)`
- `client.snapshots.list(params?)`
- `client.snapshots.retrieve(id)`
- `client.snapshots.download(id)`
- `client.snapshots.restore(id, body?)`

## Statements

- `client.statements.list(params?)`
- `client.statements.retrieve(statementId)`

## Storage

- `client.storage.createBackend(body?)`
- `client.storage.listBackends(params?)`
- `client.storage.createBucket(body?)`
- `client.storage.listBuckets(params?)`
- `client.storage.deleteBackend(id)`
- `client.storage.updateBackend(id, body?)`
- `client.storage.retrieveBackend(id)`
- `client.storage.deleteBucket(id)`
- `client.storage.updateBucket(id, body?)`
- `client.storage.retrieveBucket(id)`
- `client.storage.deleteBucketKey(id)`
- `client.storage.createBucketKey(id, body?)`
- `client.storage.listBucketKeys(id, params?)`
- `client.storage.presignBucket(id, body?)`
- `client.storage.validateBackend(id)`

## Subscriptions

- `client.subscriptions.create(body?)`
- `client.subscriptions.list(params?)`
- `client.subscriptions.retrieve(subscriptionId)`

## Tools

- `client.tools.webSearch(body?)`

## Videos

- `client.videos.generate(body?)`
- `client.videos.retrieve(generationId)`

## Webhooks

- `client.webhooks.create(body?)`
- `client.webhooks.list(params?)`
- `client.webhooks.listenRequest(options?)`
- `client.webhooks.delete(id)`
- `client.webhooks.update(id, body?)`
- `client.webhooks.retrieve(id)`
- `client.webhooks.rotateSecret(id)`
