Place this directory within the applications folder of a Web2Py installation. 

Web2Py can’t cope with a hyphen in an application name, so you will need to clone it to a directory without one, such as `collectables` for instance. To do that run `git clone 'git@github.com:timw6n/iapt-spring.git' 'collectables'` in your Web2Py applications directory.

The `master` branch is protected by GitHub branch protection so it cannot be force pushed to, changes should be made as either as incremental commits or merged with a pull request. Feature branches have no such protection.
