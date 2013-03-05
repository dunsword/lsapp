# coding=utf-8
def getMutiFormBodyData( fields, fileFields):
        #fields = {'access_token':self.accessToken}
        
        """
                     该接口用户获取提交mutiform请求表但的body，返回content_type和body对象（str）
        fields是表单的dict如{'name':'paul','type':'avatar'}
        file是用rd模式打开的文件对象列表，key是表达中fields的name，file对象在中读取并关闭{'file':imageFileObj}
        """
        BOUNDARY = '----ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for key in fields.keys():
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(fields[key])
        #for (key, filename, value) in files:
        for key in fileFields.keys():
            file=fileFields[key]
            fd=file.read()
            file.close()
            
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, file.name))
            L.append('Content-Type: %s' % 'image/jpeg')
            L.append('')            
            L.append(fd)
            L.append('--'+ BOUNDARY  )
            L.append('')
       
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body