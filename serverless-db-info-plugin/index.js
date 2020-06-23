'use strict';

const spawnSync = require('child_process').spawnSync;

class ServerlessPlugin {
  constructor(serverless, options) {
    this.serverless = serverless;
    this.options = options;
    this.commands = {
      accountsRedis: {
        usage: 'Fetches and prints out the accounts redis fqdn',
        lifecycleEvents: [
          'accountsRedis',
        ],
      },
       optoutsRedis: {
        usage: 'Fetches and prints out the optouts redis fqdn',
        lifecycleEvents: [
          'optoutsRedis',
        ],
      },
      dbUri: {
        usage: 'Fetches and prints out the dbUri',
        lifecycleEvents: [
          'dbUri',
        ],
      },
      dbUser: {
        usage: 'Fetches and prints out the dbUser',
        lifecycleEvents: [
          'dbUser',
        ],
      },
      dbPort: {
        usage: 'Fetches and prints out the dbPort',
        lifecycleEvents: [
          'dbPort',
        ],
      },
      dbHost: {
        usage: 'Fetches and prints out the dbHost',
        lifecycleEvents: [
          'dbHost',
        ],
      },
      dbPass: {
        usage: 'Fetches and prints out the dbPass',
        lifecycleEvents: [
          'dbPass',
        ],
      },
      dbName: {
        usage: 'Fetches and prints out the dbName',
        lifecycleEvents: [
          'dbName',
        ],
      },
    };

    this.hooks = {
      'dbUri:dbUri': this.dbUri.bind(this),
      'accountsRedis:accountsRedis': this.accountsRedis.bind(this),
      'optoutsRedis:optoutsRedis': this.optoutsRedis.bind(this),
      'dbHost:dbHost': this.dbHost.bind(this),
      'dbPort:dbPort': this.dbPort.bind(this),
      'dbUser:dbUser': this.dbUser.bind(this),
      'dbPass:dbPass': this.dbPass.bind(this),
      'dbName:dbName': this.dbName.bind(this),
    };
  }

  // fetches the accountsRedis FQDN
  async accountsRedis() {
    const provider = this.serverless.getProvider('aws');
    const stackName = provider.naming.getStackName(this.options.stage);
    const result = await provider.request(
      'CloudFormation',
      'describeStacks',
      { StackName: stackName },
      this.options.stage,
      this.options.region,
    );

    const outputs = result.Stacks[0].Outputs;
    const output = outputs.find(
      entry => entry.OutputKey === 'accountsRedis',
    );

    if (output && output.OutputValue) {
      this.serverless.cli.log(`accountsRedis: ${output.OutputValue}`);
      return output.OutputValue;
    }

    this.serverless.cli.log('accountsRedis Not Found');
    const error = new Error('Could not extract accountsRedis');
    throw error;
  }

  // fetches the optoutsRedis
  async optoutsRedis() {
    const provider = this.serverless.getProvider('aws');
    const stackName = provider.naming.getStackName(this.options.stage);
    const result = await provider.request(
      'CloudFormation',
      'describeStacks',
      { StackName: stackName },
      this.options.stage,
      this.options.region,
    );

    const outputs = result.Stacks[0].Outputs;
    const output = outputs.find(
      entry => entry.OutputKey === 'optoutsRedis',
    );

    if (output && output.OutputValue) {
      this.serverless.cli.log(`optoutsRedis: ${output.OutputValue}`);
      return output.OutputValue;
    }

    this.serverless.cli.log('optoutsRedis Not Found');
    const error = new Error('Could not extract optoutsRedis');
    throw error;
  }

  // fetches the db-uri
  async dbUri() {
    const provider = this.serverless.getProvider('aws');
    const stackName = provider.naming.getStackName(this.options.stage);
    const result = await provider.request(
      'CloudFormation',
      'describeStacks',
      { StackName: stackName },
      this.options.stage,
      this.options.region,
    );

    const outputs = result.Stacks[0].Outputs;
    const output = outputs.find(
      entry => entry.OutputKey === 'dbUri',
    );

    if (output && output.OutputValue) {
      this.serverless.cli.log(`dbUri: ${output.OutputValue}`);
      return output.OutputValue;
    }

    this.serverless.cli.log('dbUri Not Found');
    const error = new Error('Could not extract dbUri');
    throw error;
  }

  // fetches the db-user
  async dbUser() {
    const provider = this.serverless.getProvider('aws');
    const stackName = provider.naming.getStackName(this.options.stage);
    const result = await provider.request(
      'CloudFormation',
      'describeStacks',
      { StackName: stackName },
      this.options.stage,
      this.options.region,
    );

    const outputs = result.Stacks[0].Outputs;
    const output = outputs.find(
      entry => entry.OutputKey === 'dbUser',
    );

    if (output && output.OutputValue) {
      this.serverless.cli.log(`dbUser: ${output.OutputValue}`);
      return output.OutputValue;
    }

    this.serverless.cli.log('dbUser Not Found');
    const error = new Error('Could not extract dbUser');
    throw error;
  }

  // fetches the db-pass
  async dbPass() {
    const provider = this.serverless.getProvider('aws');
    const stackName = provider.naming.getStackName(this.options.stage);
    const result = await provider.request(
      'CloudFormation',
      'describeStacks',
      { StackName: stackName },
      this.options.stage,
      this.options.region,
    );

    const outputs = result.Stacks[0].Outputs;
    const output = outputs.find(
      entry => entry.OutputKey === 'dbPass',
    );

    if (output && output.OutputValue) {
      this.serverless.cli.log(`dbPass: ${output.OutputValue}`);
      return output.OutputValue;
    }

    this.serverless.cli.log('dbPass Not Found');
    const error = new Error('Could not extract dbPass');
    throw error;
  }

  // fetches the db-host
  async dbHost() {
    const provider = this.serverless.getProvider('aws');
    const stackName = provider.naming.getStackName(this.options.stage);
    const result = await provider.request(
      'CloudFormation',
      'describeStacks',
      { StackName: stackName },
      this.options.stage,
      this.options.region,
    );

    const outputs = result.Stacks[0].Outputs;
    const output = outputs.find(
      entry => entry.OutputKey === 'dbHost',
    );

    if (output && output.OutputValue) {
      this.serverless.cli.log(`dbHost: ${output.OutputValue}`);
      return output.OutputValue;
    }

    this.serverless.cli.log('dbHost Not Found');
    const error = new Error('Could not extract dbHost');
    throw error;
  }

  // fetches the db-port
  async dbPort() {
    const provider = this.serverless.getProvider('aws');
    const stackName = provider.naming.getStackName(this.options.stage);
    const result = await provider.request(
      'CloudFormation',
      'describeStacks',
      { StackName: stackName },
      this.options.stage,
      this.options.region,
    );

    const outputs = result.Stacks[0].Outputs;
    const output = outputs.find(
      entry => entry.OutputKey === 'dbPort',
    );

    if (output && output.OutputValue) {
      this.serverless.cli.log(`dbPort: ${output.OutputValue}`);
      return output.OutputValue;
    }

    this.serverless.cli.log('dbPort Not Found');
    const error = new Error('Could not extract dbPort');
    throw error;
  }

  // fetches the db-name
  async dbName() {
    const provider = this.serverless.getProvider('aws');
    const stackName = provider.naming.getStackName(this.options.stage);
    const result = await provider.request(
      'CloudFormation',
      'describeStacks',
      { StackName: stackName },
      this.options.stage,
      this.options.region,
    );

    const outputs = result.Stacks[0].Outputs;
    const output = outputs.find(
      entry => entry.OutputKey === 'dbName',
    );

    if (output && output.OutputValue) {
      this.serverless.cli.log(`dbName: ${output.OutputValue}`);
      return output.OutputValue;
    }

    this.serverless.cli.log('dbName Not Found');
    const error = new Error('Could not extract dbName');
    throw error;
  }
}

module.exports = ServerlessPlugin;
