import React, { useState } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import { StyleSheet, Text, View } from 'react-native';

import { fs } from '../firebase';
import { COLOURS } from '../styles/Colours';

const useConstructor = (callBack = () => {}) => {
    const [hasBeenCalled, setHasBeenCalled] = useState(false);
    if (hasBeenCalled) return;
    callBack();
    setHasBeenCalled(true);
};

const DashBoardItem = (props) => {
    const { heading, fsReference, email } = props;
    const [metric, setMetric] = useState('');
    const [metricTitle, setMetricTitle] = useState('');
    useConstructor(() => {
        // console.log('Rendering screen now');
        // Demo Account contains empty trades while email loads
        const reference = email
            ? `UserPortfolio/${email}/`
            : 'UserPortfolio/adi/';
        const docRefMetrics = collection(fs, reference, 'metrics');
        getDocs(docRefMetrics).then((doc) => {
            doc.forEach((docu) => {
                let metric_data = docu.data();
                if (docu.id == fsReference) {
                    setMetric(metric_data.value);
                    setMetricTitle(metric_data.coin);
                }
            });
        });
    });

    const getCorrectMetric = (heading) => {
        if (heading == 'Daily PnL' || heading == 'All Time PnL') {
            let modified_metric = parseFloat(metric).toFixed(2);
            if (modified_metric < 0) {
                modified_metric = Math.abs(modified_metric);
                modified_metric = '-$' + modified_metric.toString();
            } else {
                modified_metric = '$' + modified_metric.toString();
            }
            return modified_metric;
        } else if (heading == "Today's Gain" || heading == 'Platform Gain') {
            let modified_metric = parseFloat(metric).toFixed(2);
            modified_metric = modified_metric.toString() + ' %';
            return modified_metric;
        } else if (heading == 'Best Position' || heading == 'Worst Position') {
            let modified_metric = parseFloat(metric).toFixed(2);
            modified_metric =
                metricTitle + ': ' + modified_metric.toString() + ' %';
            return modified_metric;
        }
    };

    return (
        <View style={styles.mainContainer}>
            <View style={styles.rowTop}>
                <Text style={styles.heading}>{heading}</Text>
            </View>
            <View style={styles.rowBottom}>
                <Text style={styles.text}>{getCorrectMetric(heading)}</Text>
            </View>
        </View>
    );
};

export default DashBoardItem;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        backgroundColor: COLOURS.darkGrey,
        marginVertical: 2,
        borderRadius: 20,
    },
    rowTop: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        borderTopLeftRadius: 20,
        borderTopRightRadius: 20,
        borderLeftWidth: 2,
        borderTopWidth: 2,
        borderRightWidth: 2,
    },
    rowBottom: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        borderBottomLeftRadius: 20,
        borderBottomRightRadius: 20,
        borderLeftWidth: 2,
        borderBottomWidth: 2,
        borderRightWidth: 2,
    },
    heading: {
        fontFamily: 'roboto-bold',
        // fontSize: 18,
        flex: 1,
        textAlign: 'center',
    },
    text: {
        fontFamily: 'roboto',
        // fontSize: 15,
        flex: 1,
        textAlign: 'center',
    },
    green: {
        color: COLOURS.green,
    },
});
