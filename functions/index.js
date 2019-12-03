const admin = require('firebase-admin');
const functions = require('firebase-functions');

// Initalisze app with firestore
admin.initializeApp(functions.config().firebase);
let db = admin.firestore();

exports.updateStatus = functions.https.onRequest(async (request, response) => {

    const req = request
    const name = req.query.name
    const homeStatus = req.query.enteredOrExited === 'entered' ? true : false

    // Update User Status
    let userRef = await db.collection("family").doc(name)
    let resp = await userRef.update({
        isHome: homeStatus
    });

    // Add a new document with a generated id.
    await db.collection('status-history').add({
        person: name,
        input: req.query.enteredOrExited,
        isHome: homeStatus,
        timestamp: new Date()
    })

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