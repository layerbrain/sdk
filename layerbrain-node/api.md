# API Reference

## Client

- `new Layerbrain(options?)`

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

## Compute

- `client.compute.availability()`

## Events

- `client.events.create(body?)`
- `client.events.list(params?)`
- `client.events.types()`
- `client.events.retrieve(id)`

## Exports

- `client.exports.create(body?)`
- `client.exports.list(params?)`
- `client.exports.download(id)`

## Logs

- `client.logs.list(params?)`
- `client.logs.retrieve(id)`

## Machines

- `client.machines.create(body?)`
- `client.machines.list(params?)`
- `client.machines.delete(id)`
- `client.machines.retrieve(id)`
- `client.machines.connect(id)`
- `client.machines.extend(id, body?)`

## Memberships

- `client.memberships.create(body?)`
- `client.memberships.list(params?)`
- `client.memberships.delete(id)`
- `client.memberships.retrieve(id)`
- `client.memberships.update(id, body?)`

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

## Statements

- `client.statements.list(params?)`
- `client.statements.retrieve(statementId)`

## Storage

- `client.storage.createBucket(body?)`
- `client.storage.listBuckets(params?)`
- `client.storage.searchObjects()`
- `client.storage.deleteBucket(id)`
- `client.storage.updateBucket(id, body?)`
- `client.storage.retrieveBucket(id)`
- `client.storage.createBucketCredential(id, body?)`
- `client.storage.listBucketCredentials(id, params?)`
- `client.storage.createBucketFolder(id, body?)`
- `client.storage.listBucketObjects(id)`
- `client.storage.presignBucket(id, body?)`
- `client.storage.copyBucketObject(id, body?)`
- `client.storage.deleteBucketObject(id, body?)`
- `client.storage.headBucketObject(id)`
- `client.storage.moveBucketObject(id, body?)`
- `client.storage.deleteBucketCredential(id, accessKeyId)`
- `client.storage.updateBucketCredential(id, accessKeyId, body?)`

## Subscriptions

- `client.subscriptions.balance(body?)`
- `client.subscriptions.create(body?)`
- `client.subscriptions.list(params?)`
- `client.subscriptions.downgrade(body?)`
- `client.subscriptions.portal()`
- `client.subscriptions.upgrade(body?)`
- `client.subscriptions.retrieve(subscriptionId)`

## Webhooks

- `client.webhooks.create(body?)`
- `client.webhooks.list(params?)`
- `client.webhooks.listenRequest(options?)`
- `client.webhooks.delete(id)`
- `client.webhooks.update(id, body?)`
- `client.webhooks.retrieve(id)`
- `client.webhooks.listDeliveries(id, params?)`
- `client.webhooks.rotateSecret(id)`
- `client.webhooks.signingSecret(id)`
- `client.webhooks.test(id)`
- `client.webhooks.retrieveDelivery(id, deliveryId)`
