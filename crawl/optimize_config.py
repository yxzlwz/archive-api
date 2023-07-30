optimize_config = {
    'www.zhihu.com': {
        r'.*': {
            'action': 'click',
            'element': 'div.Modal.Modal--default.signFlowModal > button',
        }
    },
    'weibo.com': {
        r'.*': {
            'action': 'wait',
            'seconds': 10,
        }
    }
}

optimize_config['zhuanlan.zhihu.com'] = optimize_config['www.zhihu.com']
optimize_config['passport.weibo.com'] = optimize_config['weibo.com']
