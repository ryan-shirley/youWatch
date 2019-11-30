const admin = require('firebase-admin');
const functions = require('firebase-functions');

// Initalisze app with firestore
admin.initializeApp(functions.config().firebase);
let db = admin.firestore();

exports.updateStatus = functions.https.onRequest(async (request, response) => {

    const req = request
    const name = req.body.name
    const homeStatus = req.body.enteredOrExited === 'entered' ? true : false
    const locationMapImageUrl = req.body.locationMapImageUrl

    let resp

    let userRef = await db.collection("family").doc(name)
    resp = await userRef.update({
        isHome: homeStatus
    });

    response.send({
        data: resp,
        body: 'Congradulations 😀! You have updated your status'
    })
});


   // Working!
    // await db.collection("family").doc("ryan").get().then(doc => {
    //     if (!doc.exists) {
    //       resp = 'No such document!';
    //     } else {
    //         resp = doc.data()
    //     }
    //     return ''
    // })
    // .catch(err => {
    //     return err
    // });