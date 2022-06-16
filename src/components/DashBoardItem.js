import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { COLOURS } from '../styles/Colours';

const DashBoardItem = (props) => {
    const { heading, text } = props;
    return (
        <View style={styles.mainContainer}>
            <View style={styles.rowTop}>
                <Text style={styles.heading}>{heading}</Text>
            </View>
            <View style={styles.rowBottom}>
                <Text style={styles.text}>{text}</Text>
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
