
module.exports = {
  /**
   * Application configuration section
   * http://pm2.keymetrics.io/docs/usage/application-declaration/
   */
  apps : [
    {
      name      : 'my_react_app',
      script    : 'npm',
      args      : 'run start:production',
      env_production : {
        NODE_ENV: 'production'
      }
    },
  ],

  /**
   * Deployment section
   * http://pm2.keymetrics.io/docs/usage/deployment/
   */
  deploy : {
    production : {},
    staging: {
      user: 'your-user',
      host: '18.224.141.97',
      ref: 'origin/master',
      repo: 'git@github.com:gituser/yourrepo.git',
      path: '/var/www/yourprojectpath',
      key: '/absolute/path/to/key',
      ssh_options: ['ForwardAgent=yes'],
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production'
    },
    dev : {}
  }
};
