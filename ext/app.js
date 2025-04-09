Ext.onReady(function() {
    Ext.create('Ext.form.Panel', {
        title: 'Login',
        bodyPadding: 5,
        width: 350,
        renderTo: Ext.getBody(),
        items: [{
            xtype: 'textfield',
            name: 'username',
            fieldLabel: 'Username',
            allowBlank: false
        }, {
            xtype: 'textfield',
            name: 'password',
            fieldLabel: 'Password',
            inputType: 'password',
            allowBlank: false
        }],
        buttons: [{
            text: 'Login',
            handler: function() {
                Ext.Msg.alert('Login', 'Login button clicked');
            }
        }]
    });
});
