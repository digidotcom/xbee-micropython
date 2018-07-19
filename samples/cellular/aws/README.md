Connecting an XBee Cellular device to AWS IoT
=============================================

These samples demonstrate how to connect to AWS IoT and publish and subscribe
to topics using the `umqtt.simple` module.


Getting started with AWS IoT
----------------------------

Before running any of the samples, you'll need to add your XBee Cellular as a
"Thing" on an AWS IoT account.  Here are step-by-step instructions on how to
do that.

1. If you don't already have one, [sign up] for a "Basic" AWS account with 12
   months of free tier access.  You can add devices and generate certificates,
   but they might not be able to connect until you receive email from Amazon
   confirming that your AWS account is ready.
   
2. Once you have an AWS account, log into the [AWS IoT Console].

3. Create a policy for access control.  Click on **Secure**, then **Policies**
   and then the **Create** button.  Click on the **Advanced Mode** link to
   allow pasting a full policy.

   These samples include two policies you can use as a starting point.

   One is an [open policy](./policy-open.json) without any restrictions.  We
   recommend starting with that until you have a working connection.
   
   The other is a [restricted policy](./policy-restricted.json) that requires
   clients to use their ThingName as the ClientId, and only allows
   Publish/Subscribe to topics under a `{ThingType}/{ThingName}` hierarchy.  Be
   sure to update the ARNs with your region and AWS account number.  Note that
   it doesn't include a configuration for the Device Shadow Service used for
   testing from the [HTTPS Sample](./aws-https.py).

[sign up]: https://portal.aws.amazon.com/billing/signup#/start
[AWS IoT Console]: https://console.aws.amazon.com/iot/home


Create a "Thing" on AWS IoT
---------------------------
1. Click on the **Manage** menu and select **Things** to Register a Thing.

2. Give a unique name to your device, and create an "XBee_Cellular" type
   with an "IMEI" Attribute key you can use to identify a specific module
   in case you add multiple modules to your AWS account.  You can get the
   XBee Cellular's IMEI with the `ATIM` command.

3. Once you've created your thing, use One-click certificate creation to
   generate a certificate, public key and private key for your device.

4. Download the certificate and private key for this specific device.  We
   won't be using the public key file, so you don't need to download it.
   You can download it from AWS later if you need it for some other reason.

5. You'll also need a CA for AWS IoT (this file should be identical for all
   devices you connect to your account).  Be sure to download it before
   activating your device.

6. Attach the policy you previously created, and that completes the activation
   process.


Install the certificates on XBee Cellular
-----------------------------------------
Place the downloaded certificates into a folder on your computer with a name
to match your Thing's name or the 10-character ID used in the file names (which
correspond to the start of the certificate's ID shown in the AWS IoT console).

To simplify file management on your XBee Cellular and to allow re-use of the
same code on multiple devices, give your files shorter names (we use these
names in the included samples):

| Original Filename                                        | Shortened Name |
|----------------------------------------------------------|----------------|
| 01234abcde-certificate.pem.crt                                 | aws.crt  |
| 01234abcde-private.pem.key                                     | aws.key* |
| VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem | aws.ca   |

Use XCTU or ATFS commands in a terminal emulator to upload the three files
to the `cert/` directory on your XBee.

*For security, you should upload the `aws.key` as a secure file (using
`ATFS XPUT`).


Test the Certificates
---------------------
Update the [HTTPS Sample](./aws-https.py) with details on your Thing and use
it to test the certificates you uploaded.  All samples will use the same
settings so you can easily paste your configuration to the top of each sample.

You can find the host and region for your Rest API Endpoint by clicking on
**Interact** when looking at your Thing in the AWS IoT Console.

You should see output like this after running the sample.  The 92 is the
result of the `w.write()` call (92 bytes written) and the blank lines come
from the CR/LF line endings used in HTTP connections.

```
92
HTTP/1.1 200 OK
 
content-type: application/json
 
content-length: 61
 
date: Thu, 05 Jul 2018 19:28:03 GMT
 
x-amzn-RequestId: 0744caf6-2162-1d4f-c4f9-67a2d7ff2ce9
 
connection: keep-alive
 
 
 
{"state":{},"metadata":{},"version":1,"timestamp":1530818883}
```


Publish to a topic
------------------
Use the [Publish Sample](./aws-publish.py) to publish data to an MQTT topic.
Remember to update the configuration section of the sample with values that
match your account/Thing.

You can monitor all topics from the AWS IoT Console.  Click on the **Test**
option and subscribe to the topic `#` to see all messages pushed to your
account in real time.

You can also navigate to your Thing and click on **Activity** to monitor when
your Thing makes an MQTT connection and then disconnects.


Subscribe to a topic
--------------------
Use the [Subscribe Sample](./aws-subscribe.py) to monitor an MQTT topic that
you will push to from a separate MQTT client.

View the sample for details on how to configure and use it.


Publish and Subscribe
---------------------
The [Temp Sensor Sample](./aws-tempsensor.py) integrates MQTT publishing and
subscribing, in addition to using an HDC1080 I2C Temp & Humidity Sensor as the
source for published data.

View the sample for details on how to configure and use it.
