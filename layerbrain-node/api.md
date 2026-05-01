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
- `client.brains.list(params?)`
- `client.brains.delete(id)`
- `client.brains.retrieve(id)`
- `client.brains.archive(id)`

## Chat

- `client.chat.completions.create(params)`

## Compute

- `client.compute.computeDisabled()`
- `client.compute.createComputeDisabled(body?)`
- `client.compute.updateComputeDisabled(body?)`
- `client.compute.deleteComputeDisabled()`
- `client.compute.computePathDisabled(path)`
- `client.compute.createComputePathDisabled(path, body?)`
- `client.compute.updateComputePathDisabled(path, body?)`
- `client.compute.deleteComputePathDisabled(path)`

## Embeddings

- `client.embeddings.create(body?)`

## Events

- `client.events.list(params?)`
- `client.events.retrieve(id)`

## Exports

- `client.exports.create(body?)`
- `client.exports.list(params?)`
- `client.exports.download(id)`

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
- `client.memberships.delete(id)`
- `client.memberships.retrieve(id)`
- `client.memberships.update(id, body?)`

## Models

- `client.models.list(params?)`
- `client.models.retrieve(modelId)`

## Organizations

- `client.organizations.create(body?)`
- `client.organizations.list(params?)`
- `client.organizations.delete(id)`
- `client.organizations.retrieve(id)`
- `client.organizations.update(id, body?)`

## Plans

- `client.plans.create(body?)`
- `client.plans.list(params?)`
- `client.plans.update(id, body?)`
- `client.plans.retrieve(id)`
- `client.plans.addItems(id, body?)`
- `client.plans.deleteItems(id)`
- `client.plans.updateItems(id, body?)`
- `client.plans.cancel(id, body?)`
- `client.plans.createComment(id, body?)`
- `client.plans.listComments(id, params?)`
- `client.plans.listActivity(id, params?)`
- `client.plans.resume(id, body?)`
- `client.plans.start(id, body?)`
- `client.plans.createItemComment(id, item, body?)`
- `client.plans.listItemComments(id, item, params?)`
- `client.plans.listItemActivity(id, item, params?)`

## Secrets

- `client.secrets.create(body?)`
- `client.secrets.list(params?)`
- `client.secrets.delete(id)`
- `client.secrets.update(id, body?)`
- `client.secrets.retrieve(id)`
- `client.secrets.reveal(id)`

## Snapshots

- `client.snapshots.snapshotsDisabled()`
- `client.snapshots.createSnapshotsDisabled(body?)`
- `client.snapshots.updateSnapshotsDisabled(body?)`
- `client.snapshots.deleteSnapshotsDisabled()`
- `client.snapshots.snapshotsPathDisabled(path)`
- `client.snapshots.createSnapshotsPathDisabled(path, body?)`
- `client.snapshots.updateSnapshotsPathDisabled(path, body?)`
- `client.snapshots.deleteSnapshotsPathDisabled(path)`

## Statements

- `client.statements.list(params?)`
- `client.statements.retrieve(statementId)`

## Storage

- `client.storage.createBucket(body?)`
- `client.storage.listBuckets(params?)`
- `client.storage.searchStorageObjects()`
- `client.storage.deleteBucket(id)`
- `client.storage.updateBucket(id, body?)`
- `client.storage.retrieveBucket(id)`
- `client.storage.deleteBucketKey(id)`
- `client.storage.createBucketFolder(id, body?)`
- `client.storage.createBucketKey(id, body?)`
- `client.storage.listBucketKeys(id, params?)`
- `client.storage.listBucketObjects(id, params?)`
- `client.storage.presignBucket(id, body?)`
- `client.storage.copyBucketObject(id, body?)`
- `client.storage.deleteBucketObject(id, body?)`
- `client.storage.headBucketObject(id)`
- `client.storage.moveBucketObject(id, body?)`

## Subscriptions

- `client.subscriptions.create(body?)`
- `client.subscriptions.list(params?)`
- `client.subscriptions.retrieve(subscriptionId)`

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
- `client.webhooks.deliveries(id)`
- `client.webhooks.rotateSecret(id)`
- `client.webhooks.signingSecret(id)`
- `client.webhooks.test(id, body?)`
- `client.webhooks.delivery(id, deliveryId)`

## Work

- `client.work.list(params?)`
- `client.work.retrieve(id)`
