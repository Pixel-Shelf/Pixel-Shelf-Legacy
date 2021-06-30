var express = require('express');
var router = express.Router();
var SQLite3Driver = require('../models/SQLite3Driver');
var IGDBDriver = require('../models/IGDBDriver');
var EInkDriver = require('../eink/EInkDriver');

router.get('/', function (req, res, next) {
    res.status(200).send({"status": 200});
});

router.get('/library', function (req, res, next) {
    let sortBy = req.query.sortBy;
    if (sortBy === null) {
        sortBy = 'title';
    }
    let driver = new SQLite3Driver();
    driver.getLibrary(sortBy).then(result => {
        res.status(200).send({"status": 200, "library": result});
    }).catch(err => {
        sendError(res, err);
    });
});


router.get('/library/size', function (req, res, next) {
    let driver = new SQLite3Driver();
    if (req.query.by === 'platform') {
        res.status(500).send({"status": 501, "msg": "Not implemented!"});
    } else {
        driver.getLibrarySize().then(result => {
            res.status(200).send({"status": 200, "size": result});
        }).catch(err => {
            sendError(res, err);
        });
    }
});

router.get('/library/:libraryId/igdb', function (req, res, next) {
    let driver = new SQLite3Driver();
    const libraryId = req.params.libraryId;
    driver.getLibraryGame(libraryId).then(result => {
        if (result.igdbURL != null) {
            let igdbDriver = new IGDBDriver();
            igdbDriver.getGameByURL(result.igdbURL).then(igdbRes => {
                res.status(200).send({"status": 200, "data": igdbRes});
            }).catch(err => {
                sendError(res, err);
            });
        }
    }).catch(err => {
        sendError(res, err);
    });
});

router.delete('/library/:libraryId', function (req, res, next) {
    let driver = new SQLite3Driver();
    driver.deleteGame(req.params.libraryId).then(result => {
        res.status(204).send({"status": 204});
    }).catch(err => {
        sendError(res, err);
    });
});

router.get('/wishlist', function (req, res, next) {
    let sortBy = req.query.sortBy;
    if (sortBy === null) {
        sortBy = 'title';
    }
    let driver = new SQLite3Driver();
    driver.getWishlist(sortBy).then(result => {
        res.status(200).send({"status": 200, "library": result});
    }).catch(err => {
        sendError(res, err);
    });
});

router.post('/games', function (req, res) {
    let driver = new SQLite3Driver();
    driver.lookupGame(req.body.title, req.body.platform).then(gameResult => {
        if (gameResult.found === true) {
            res.status(200).send({"status": 200, "id": gameResult.id, "igdb": gameResult.igdb});
        } else {
            let igdbDriver = new IGDBDriver();
            igdbDriver.getGameByName(req.body.title).then(result => {
                console.log(result)
                let igdbLink;
                if (result.length < 1) {
                    igdbLink = null;
                } else {
                    igdbLink = result[0].url;
                }
                driver.addGame({
                    "title": req.body.title,
                    "platform": req.body.platform,
                    "igdb-url": igdbLink
                }).then(addResult => {
                    res.status(200).send({"status": 200, "id": addResult, "igdb": igdbLink});
                    igdbDriver.getCoverByURL(igdbLink, addResult).catch(err => {
                        console.log(err);
                    });
                }).catch(err => {
                    sendError(res, err);
                })
            }).catch(err => {
                sendError(res, err);
            });
        }
    }).catch(err => {
        sendError(res, err);
    });
});

router.post('/editions', function (req, res) {
    let driver = new SQLite3Driver();
    console.log(req.body);
    driver.lookupEdition(req.body.edition, req.body.gameID).then(result => {
        if (result.found === true) {
            res.status(200).send({"status": 200, "id": result.id});
        } else {
            driver.addEdition(req.body).then(addResult => {
                res.status(200).send({"status": 200, "id": addResult});
            }).catch(err => {
                sendError(res, err);
            })
        }
    }).catch(err => {
        sendError(res, err);
    });
});

router.post('/library', function (req, res) {
    let driver = new SQLite3Driver();
    console.log(req.body);
    driver.addLibrary(req.body).then(addResult => {
        res.status(200).send({"status": 200, "id": addResult});
    }).catch(err => {
        sendError(res, err);
    })
});

router.post('/wishlist', function (req, res) {
    let driver = new SQLite3Driver();
    console.log(req.body);
    driver.addWishlist(req.body).then(addResult => {
        res.status(200).send({"status": 200, "id": addResult});
    }).catch(err => {
        sendError(res, err);
    })
});

function sendError(res, err) {
    res.status(500).send({"status": 500, "error": err});
}

module.exports = router;
