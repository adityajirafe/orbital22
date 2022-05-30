import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

const DashBoardItem = props => {
    const {heading, text} = props
    return (
        <View style = {[styles.mainContainer, styles.boxColour]}>
            <View style = {styles.row}>
                <Text style = {styles.heading}>{heading}</Text>
            </View>
            <View style = {styles.row}>
                <Text style = {styles.text}>{text}</Text>
            </View>
        </View>
    )
}

export default DashBoardItem

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        borderWidth: 10,
        borderColor: '#c8dfe4'
    },
    row: {
        flex: 1,
        padding: 0,
        // alignContent: 'center',
        alignItems: 'center',
        padding: 10,
    },
    heading: {
        fontFamily: 'roboto-bold',
        fontSize: 18,
        flex: 1,
    },
    text: {
        fontFamily: 'roboto',
        fontSize: 15,
        flex: 1,
    },
    green: {
        color: 'green'
    },
    boxColour: {
        backgroundColor: 'lightblue'
    }
})