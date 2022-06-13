import { StyleSheet } from 'react-native';
import { COLOURS } from './Colours';

export const globalStyles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: COLOURS.background,
    },
    blankContainer: {
        flex: 0.5,
        backgroundColor: COLOURS.background,
    },
    container_auth: {
        backgroundColor: COLOURS.background,
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    container_signup: {
        backgroundColor: COLOURS.background,
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingTop: 20,
    },
    main: {
        flex: 1,
        backgroundColor: COLOURS.white,
        alignContent: 'center',
        alignItems: 'center',
    },
    title: {
        textAlign: 'center',
        color: 'white',
        fontFamily: 'roboto-bold',
        fontSize: 60,
        fontWeight: 'bold',
    },
    boldText: {
        fontFamily: 'roboto-bold',
    },
    coinValet_title: {
        fontFamily: 'advent',
        fontSize: 72,
        color: 'black',
    },
    welcomeText: {
        fontSize: 20,
        textAlign: 'center',
        marginBottom: 20,
        fontFamily: 'roboto-bold',
    },
    text: {
        fontFamily: 'roboto',
        fontSize: 20,
    },
    logoutIcon: {
        paddingRight: 10,
    },
});
